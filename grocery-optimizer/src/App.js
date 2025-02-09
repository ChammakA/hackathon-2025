import React, {useState} from 'react';
import GroceryForm from './components/GroceryComponent';
import Results from './components/Results';
import axios from 'axios';

const App = () => {
    const [results, setResults] = useState([]);

    const handleSearch = async (data) => {
        try {
            const response = await axios.post("http://127.0.0.1:5000/scrape-prices", data);
            console.log(response.data);
            setResults(response.data);
        } catch (error) {
            console.error("Error fetching data", error);
        }
    };

    return (
        <div className='container'>
            <h1 className='mt-4 text-center'>Grocery Optimizer</h1>
            <GroceryForm onSearch={handleSearch} />
            <Results results={results} />
        </div>
    );
};

export default App;