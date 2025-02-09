import React, {useState} from 'react';

const GroceryForm = ({onSearch}) => {
    const [groceryList, setGroceryList] = useState([]);
    const [budget, setBudget] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        onSearch({items : groceryList, budget});
    }

    return (
        <div className='container mt-4'>
            <h2>Compare Grocery Prices and Healthiest Options</h2>
            <form onSubmit={handleSubmit}>
                <label>Enter Grocery Item (comma separated):</label>
                <input
                    type = "text"
                    className='form-control'
                    onChange={(e) => setGroceryList(e.target.value.split(','))}
                    placeholder="e.g., apple, tomato, bread"
                />

                <label className='mt-3'>Enter your budger:</label>
                <input
                    type = "text"
                    className='form-control'
                    onChange={(e) => setBudget(e.target.value)}
                    placeholder="e.g., 100"
                />

                <button type="submit" className='btn btn-primary mt-3'>Submit</button>
            </form>
        </div>
    );
};

export default GroceryForm;