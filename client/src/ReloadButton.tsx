import React, {useState} from 'react';
import LoadingButton from '@mui/lab/LoadingButton';
import CircularProgress from '@mui/material/CircularProgress';
import axios from 'axios';

const ReloadButton: React.FC = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [isSuccess, setIsSuccess] = useState(false);

    const handleReload = async () => {
        setIsLoading(true);
        setIsSuccess(false);
        try {
            await axios.get('http://localhost:8000/wahlkreis/reload');
            setIsSuccess(true);
        } catch (error) {
            console.error('Reload failed:', error);
        }
        setIsLoading(false);
    };

    return (
        <div>
            <LoadingButton
                loading={isLoading}
                loadingPosition="start"
                startIcon={isLoading ? <CircularProgress color="inherit" size={16}/> : null}
                variant="contained"
                color="primary"
                onClick={handleReload}
                disabled={isLoading}
            >
                {isSuccess ? 'Reloading successful' : 'Reload'}
            </LoadingButton>
        </div>
    );
};

export default ReloadButton;