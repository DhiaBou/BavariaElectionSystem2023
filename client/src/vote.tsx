import React, { useState } from 'react';
import { TextField, Button, FormControl, RadioGroup, FormControlLabel, Radio } from '@mui/material';
import axios from 'axios';

const VotingComponent = () => {
  const [voter_id, setVoter_id] = useState('');
  const [code, setCode] = useState('');
  const [token, setToken] = useState('');
  const [firstVoteCandidates, setFirstVoteCandidates] = useState([]);
  const [secondVoteCandidates, setSecondVoteCandidates] = useState([]);
  const [selectedFirstVote, setSelectedFirstVote] = useState('');
  const [selectedSecondVote, setSelectedSecondVote] = useState('');
  const [error, setError] = useState('');

  // @ts-ignore
  const handleVoterIdChange = (event) => {
    setVoter_id(event.target.value);
  };

  // @ts-ignore
  const handleCodeChange = (event) => {
    setCode(event.target.value);
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
        params: { voter_id, code }
      });
      // Assuming the response returns two lists for first and second votes
      setToken(response.data[0]);
      setFirstVoteCandidates(response.data[1]);
      setSecondVoteCandidates(response.data[2]);
      setError('');
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
      code,
      first_vote: selectedFirstVote,
      second_vote: selectedSecondVote,
    });
    console.log("Vote submitted successfully");
  } catch (err) {
    console.error("Error submitting vote", err);
  }
};

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Voter ID"
          value={voter_id}
          onChange={handleVoterIdChange}
          margin="normal"
          variant="outlined"
        />
        <TextField
          label="Code"
          type="password"
          value={code}
          onChange={handleCodeChange}
          margin="normal"
          variant="outlined"
        />
        <Button type="submit" variant="contained" color="primary">
          Submit
        </Button>
      </form>

      {firstVoteCandidates.length > 0 && (
        <FormControl component="fieldset">
          <RadioGroup
            name="firstVoteCandidates"
            value={selectedFirstVote}
            onChange={handleFirstVoteChange}
          >
            {firstVoteCandidates.map((candidateId) => (
              <FormControlLabel
                key={candidateId}
                value={String(candidateId)}
                control={<Radio />}
                label={`${candidateId}`}
              />
            ))}
          </RadioGroup>
        </FormControl>
      )}

      {secondVoteCandidates.length > 0 && (
        <FormControl component="fieldset">
          <RadioGroup
            name="secondVoteCandidates"
            value={selectedSecondVote}
            onChange={handleSecondVoteChange}
          >
            {secondVoteCandidates.map((candidateId) => (
              <FormControlLabel
                key={candidateId}
                value={String(candidateId)}
                control={<Radio />}
                label={`${candidateId}`}
              />
            ))}
          </RadioGroup>
        </FormControl>
      )}

      <Button
        variant="contained"
        color="primary"
        onClick={handleVoteSubmit}
        disabled={!selectedFirstVote || !selectedSecondVote}
      >
        Vote
      </Button>

      {error && <p>{error}</p>}
    </div>
  );
};

export default VotingComponent;
