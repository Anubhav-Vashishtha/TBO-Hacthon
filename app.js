import express from 'express'
import { makeAuthenticatedRequest } from './Helper Function/authen.js'

const app = express();
app.use(express.json());

app.get('/send', async (req, res) => {
    try {
        const requestData = {
            "Hotelcodes": 1000957, "Language": "en"
            }; 

        const data = await makeAuthenticatedRequest('/Hoteldetails', 'post', requestData);
        res.json({ message: 'Success', data });
    } catch (error) {
        res.status(500).json({ error: 'Failed to send data' });
    }
});

const PORT = process.env.PORT;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
