import express from 'express';
import { makeAuthenticatedRequest } from './Helper Function/authen.js';

const app = express();

// Middleware
app.set('view engine', 'pug');
app.set('views', './views');
app.use(express.static('public'));
app.use(express.json());
app.use(express.urlencoded({ extended: true })); // Parse form data

// Routes
app.get('/', (req, res) => {
    res.render('send', { title: 'Hotel Search' });
});

app.post('/hotel', (req, res) => {
    const { city, state, message } = req.body;
    console.log(req.body); 
    res.send(`Form submitted! City: ${city}, State: ${state}, Message: ${message}`);
});

// Start Server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
