import express from 'express';
import { makeAuthenticatedRequest } from './Helper Function/authen.js';

const app = express();

app.set('view engine', 'pug');
app.set('views', './views');
app.use(express.static('public'));
app.use(express.json());

app.get('/send', async (req, res) => {
    try {
        const requestData = {
            "Hotelcodes": 1000957,
            "Language": "en"
        };

        const data = await makeAuthenticatedRequest('/Hoteldetails', 'post', requestData);
        // res.json({ message: 'Success', data });
        res.render('send', { title: 'Send Data', message: 'Submit your request' });
    } catch (error) {
        res.status(500).json({ error: 'Failed to send data' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
