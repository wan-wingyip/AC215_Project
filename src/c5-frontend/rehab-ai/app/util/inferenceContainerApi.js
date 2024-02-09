import axios from 'axios';

// Function to replace the image URL ending from 's.jpg' to 'od.jpg'
const getUpdatedImageUrl = (url) => {
    if (!url) return '';
    return url.replace('s.jpg', 'od.jpg');
};

// fetches labels from C4 container
export const fetchLabels = (properties) => {
    return new Promise(async (resolve, reject) => {
        const payload = properties.reduce((acc, property) => {
            if (property.primary_photo && property.property_id) {
                const updatedImageUrl = getUpdatedImageUrl(property.primary_photo.href);
                acc[property.property_id] = [updatedImageUrl];
            }
            return acc;
        }, {});

        const start = performance.now();

        try {
            const response = await axios.post(process.env.NEXT_PUBLIC_INFERENCE_URL, payload);
            const end = performance.now();
            const timeTaken = end - start;

            console.log('Response from labeling API:', response.data);
            console.log('Time elapsed:', timeTaken);

            resolve(response.data); // Resolving with the response data
        } catch (error) {
            const end = performance.now();
            const timeTaken = end - start;
            console.error('Error sending data to labeling API after ' + timeTaken +':', error);
            reject(error); // Rejecting the promise in case of error
        }
    });
};


