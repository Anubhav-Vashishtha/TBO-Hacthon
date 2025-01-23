import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const USERNAME = process.env.API_USERNAME;
const PASSWORD = process.env.API_PASSWORD;
const BASE_URL = process.env.BASE_URL;

export const makeAuthenticatedRequest = async (endpoint, method , requestData = null) => {
    console.log('Done')
    try {
        const authHeader = 'Basic ' + Buffer.from(`${USERNAME}:${PASSWORD}`).toString('base64');
        const response = await axios({
            url: `${BASE_URL}${endpoint}`,
            method: method,
            headers: {
                'Authorization': authHeader,
                'Content-Type': 'application/json'
            },
            data: requestData || {}  
        });
        return response.data;
    } catch (error) {
        console.error('Error making request:', error.response ? error.response.data : error.message);
        throw error;
    }
};
