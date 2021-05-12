const axios = require('axios').default;

export async function documentPreview(id) {
    try {
        const response = await axios.get('/documentPreview', {
            params: {
                id: id
            }
        })
        return response
    } catch (err) {
        console.error(err);
    }
}

export async function search(query) {
    try {
        const response = await axios.get('/search', {
            params: {
                query: query
            }
        })
        return response
    } catch (err) {
        console.error(err);
    }
}

