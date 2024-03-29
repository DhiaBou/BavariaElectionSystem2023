import React, {useState} from 'react';
import {
    Button,
    Card,
    CardContent,
    FormControlLabel,
    Grid,
    Radio,
    RadioGroup,
    TextField,
    Typography
} from '@material-ui/core';
import axios from 'axios';

const VotingComponent = () => {
    const [voter_id, setVoter_id] = useState('');
    const [stimmkreis, setStimmkreis] = useState('');
    const [token, setToken] = useState('');
    const [firstVoteCandidates, setFirstVoteCandidates] = useState([]);
    const [secondVoteCandidates, setSecondVoteCandidates] = useState([]);
    const [selectedFirstVote, setSelectedFirstVote] = useState('');
    const [selectedSecondVote, setSelectedSecondVote] = useState('');
    const [error, setError] = useState('');
    const [currentStep, setCurrentStep] = useState(1); // 1 for first vote, 2 for second vote, 3 for completed

    // @ts-ignore
    const handleVoterIdChange = (event) => {
        setVoter_id(event.target.value);
    };

    // @ts-ignore
    const handleCodeChange = (event) => {
        setStimmkreis(event.target.value);
    };

    // @ts-ignore
    const handleFirstVoteChange = (event) => {
        setSelectedFirstVote(event.target.value);
    };

    // @ts-ignore
    const handleSecondVoteChange = (event) => {
        setSelectedSecondVote(event.target.value);
    };

    // @ts-ignore
    const handleCheck = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.get('http://localhost:8000/vote', {
                params: {voter_id, code: stimmkreis}
            });

            setToken(response.data[0]);
            setFirstVoteCandidates(response.data[1]);
            setSecondVoteCandidates(response.data[2]);
            setError('');
            setCurrentStep(3);


        } catch (err) {
            setError('Error: Unable to fetch candidates.');
            setFirstVoteCandidates([]);
            setSecondVoteCandidates([]);

        }
    };

    const handleSubmitVote = async () => {
        try {
            await axios.post('http://localhost:8000/vote/submit_vote', {
                token,
                code: stimmkreis,
                first_vote: selectedFirstVote,
                second_vote: selectedSecondVote,
            });
            console.log("Second vote submitted successfully");
            setCurrentStep(4);
        } catch (err) {
            console.error("Error submitting second vote", err);
        }
    };
    if (currentStep === 1) {
        return (
            <div style={{padding: '20px', maxWidth: '500px', margin: 'auto'}}>
                <form onSubmit={handleCheck}>
                    <Grid container spacing={2} alignItems="center">
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                label="Wähler ID"
                                value={voter_id}
                                onChange={handleVoterIdChange}
                                margin="normal"
                                variant="outlined"
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                label="Stimmkreis"
                                value={stimmkreis}
                                onChange={handleCodeChange}
                                margin="normal"
                                variant="outlined"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <Button
                                type="submit"
                                variant="contained"
                                color="primary"
                                fullWidth
                            >
                                Anmelden
                            </Button>
                        </Grid>
                    </Grid>
                </form>

                {error && <p>{error}</p>}
            </div>
        );
    } else if (currentStep === 3) {
        return (
            <div style={{padding: '20px', maxWidth: '1000px', margin: 'auto'}}>
                {/* Second Vote Section */}
                <div style={{display: 'flex', justifyContent: 'space-between'}}>
                    {firstVoteCandidates.length > 0 && (
                        <Card className="vote-section" style={{overflow: 'auto', height: '600px'}}>
                            <CardContent>
                                <Typography variant="h5" component="h2">
                                    Erststimme
                                </Typography>
                                <RadioGroup name="firstVoteCandidates" value={selectedFirstVote}
                                            onChange={handleFirstVoteChange}>
                                    {firstVoteCandidates.map(candidate => (
                                        <FormControlLabel
                                            key={candidate}
                                            value={String(candidate).split('__')[1]}
                                            control={<Radio/>}
                                            label={String(candidate).split('__')[0]}
                                        />
                                    ))}
                                </RadioGroup>
                            </CardContent>
                        </Card>
                    )}
                    {secondVoteCandidates.length > 0 && (
                        <div style={{marginLeft: '50px', flex: '1'}}>
                            <Card className="vote-section" style={{overflow: 'auto', height: '600px'}}>
                                <CardContent>
                                    <Typography variant="h5" component="h2">
                                        Zweitstimme
                                    </Typography>
                                    <RadioGroup name="secondVoteCandidates" value={selectedSecondVote}
                                                onChange={handleSecondVoteChange}>
                                        {secondVoteCandidates.map(candidate => (
                                            <FormControlLabel
                                                key={candidate}
                                                value={String(candidate).split('__')[1]}
                                                control={<Radio/>}
                                                label={String(candidate).split('__')[0]}
                                            />
                                        ))}
                                    </RadioGroup>
                                </CardContent>
                            </Card></div>
                    )}

                </div>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleSubmitVote}
                    disabled={!selectedSecondVote && !selectedFirstVote}
                    fullWidth
                >
                    Stimme abgeben
                </Button>

                {error && <p>{error}</p>}
            </div>
        );
    } else {
        return (
            <div style={{padding: '20px', maxWidth: '500px', margin: 'auto'}}>
                <Typography variant="h5">Danke!</Typography>
            </div>
        );
    }
};
export default VotingComponent;

