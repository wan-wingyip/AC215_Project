import axios from 'axios';

// Fetches a list of properties based on the provided zipcode
export const fetchPropertyList = async (zipcode) => {

    const options = {
        method: 'POST',
        url: process.env.NEXT_PUBLIC_REALTY_API_URL,
        headers: {
        'content-type': 'application/json',
        'X-RapidAPI-Key': process.env.NEXT_PUBLIC_RAPID_API_KEY, // set .env file in root of project w/ secret key
        'X-RapidAPI-Host': 'realty-in-us.p.rapidapi.com'
        },
        data: {
        limit: 10,
        offset: 0,
        postal_code: zipcode,
        year_built: {"max": 2023,"min": 1300},
        status: ['for_sale'],
        sort: {
            direction: 'desc',
            field: 'list_date'
        }
        }
    };
    const start = performance.now();

    try {
        const response = await axios.request(options);
        const end = performance.now();
        console.log("Response from property list API:", response.data);
        const timeTaken = end - start;
        console.log('Time elapsed:', timeTaken);
        return response.data; // Return the response data
    } catch (error) {
        const end = performance.now();
        const timeTaken = end - start;
        console.log('Error fetching data after ' + timeTaken +':', error);
        return null; // Return null or handle the error as needed
    }
};