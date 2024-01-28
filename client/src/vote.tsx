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
    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.get('http://localhost:8000/vote', {
                params: {voter_id, code: stimmkreis}
            });
            // Assuming the response returns two lists for first and second votes

            setToken(response.data[0]);
            setFirstVoteCandidates(response.data[1]);
            setSecondVoteCandidates(response.data[2]);
            setError('');
            setCurrentStep(2); // Move to second vote


        } catch (err) {
            setError('Error: Unable to fetch candidates.');
            setFirstVoteCandidates([]);
            setSecondVoteCandidates([]);

        }
    };

    const handleVoteSubmit = async () => {
        try {
            await axios.post('http://localhost:8000/vote/submit_vote', {
                token,
                code: stimmkreis,
                first_vote: selectedFirstVote,
                second_vote: selectedSecondVote,
            });
            console.log("Vote submitted successfully");
        } catch (err) {
            console.error("Error submitting vote", err);
        }
    };
    const handleFirstVoteSubmit = async () => {
        try {
            // Submit the first vote
            // Assuming the API endpoint and request body for first vote submission
            await axios.post('http://localhost:8000/vote/first_vote', {
                token,
                code: stimmkreis,
                first_vote: selectedFirstVote,
            });

            console.log("First vote submitted successfully");
            setCurrentStep(3); // Move to second vote
        } catch (err) {
            console.error("Error submitting first vote", err);
        }
    };
    const handleSecondVoteSubmit = async () => {
        try {
            // Submit the second vote
            await axios.post('http://localhost:8000/vote/second_vote', {
                token,
                code: stimmkreis,
                second_vote: selectedSecondVote,
            });
            console.log("Second vote submitted successfully");
            setCurrentStep(4); // Voting completed
        } catch (err) {
            console.error("Error submitting second vote", err);
        }
    };
    if (currentStep === 1) {
        return (
            <div style={{padding: '20px', maxWidth: '500px', margin: 'auto'}}>
                <form onSubmit={handleSubmit}>
                    <Grid container spacing={2} alignItems="center">
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                label="Voter ID"
                                value={voter_id}
                                onChange={handleVoterIdChange}
                                margin="normal"
                                variant="outlined"
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                label="Code"
                                type="password"
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
                                Identify
                            </Button>
                        </Grid>
                    </Grid>
                </form>

                {error && <p>{error}</p>}
            </div>
        );
    }
    if (currentStep === 2) {
        return (
            <div style={{padding: '20px', maxWidth: '500px', margin: 'auto'}}>
                {/* First Vote Section */}
                {firstVoteCandidates.length > 0 && (
                    <Card className="vote-section">
                        <CardContent>
                            <Typography variant="h5" component="h2">
                                First Vote
                            </Typography>
                            <RadioGroup name="firstVoteCandidates" value={selectedFirstVote}
                                        onChange={handleFirstVoteChange}>
                                {firstVoteCandidates.map(candidate => (
                                    <FormControlLabel
                                        key={candidate}
                                        value={String(candidate)}
                                        control={<Radio/>}
                                        label={candidate}
                                    />
                                ))}
                            </RadioGroup>
                        </CardContent>
                    </Card>
                )}
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleFirstVoteSubmit}
                    disabled={!selectedFirstVote}
                    fullWidth
                >
                    Submit First Vote
                </Button>

                {error && <p>{error}</p>}
            </div>
        );
    } else if (currentStep === 3) {
        return (
            <div style={{padding: '20px', maxWidth: '500px', margin: 'auto'}}>
                {/* Second Vote Section */}
                {secondVoteCandidates.length > 0 && (
                    <Card className="vote-section">
                        <CardContent>
                            <Typography variant="h5" component="h2">
                                Second Vote
                            </Typography>
                            <RadioGroup name="secondVoteCandidates" value={selectedSecondVote}
                                        onChange={handleSecondVoteChange}>
                                {secondVoteCandidates.map(candidate => (
                                    <FormControlLabel
                                        key={candidate}
                                        value={String(candidate)}
                                        control={<Radio/>}
                                        label={candidate}
                                    />
                                ))}
                            </RadioGroup>
                        </CardContent>
                    </Card>
                )}
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleSecondVoteSubmit}
                    disabled={!selectedSecondVote}
                    fullWidth
                >
                    Submit Second Vote
                </Button>

                {error && <p>{error}</p>}
            </div>
        );
    } else {
        return (
            <div style={{padding: '20px', maxWidth: '500px', margin: 'auto'}}>
                <Typography variant="h5">Thank you for voting!</Typography>
            </div>
        );
    }
};
export default VotingComponent;

