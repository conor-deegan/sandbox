const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());

app.get('/message/:account', async (req, res) => {
    try {
        res.status(200).json('got it');
    } catch (error) {
        res.error(error);
    }
});

app.listen(8080, () => {
    console.log('SERVER LISTENING ON PORT 8080');
});