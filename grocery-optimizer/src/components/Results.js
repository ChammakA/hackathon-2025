import React from 'react';

const Results = ({results}) => {
    return (
        <div className='container mt-4'>
            <h2>Results</h2>
            {results.length > 0 ? (
                <ul className='list-group'>
                    {results.map((item, index) => (
                        <li key={index} className='list-group-item'>
                            <strong>{item.item}</strong>
                            <br />
                            <span>Cheapest: {item.cheapest_option.price} at {item.cheapest_option.store}</span>
                            <br />
                            <span>Healthiest: {item.healthiest_option?.food_name || "N/A"} ({item.healthiest_option?.brand || ""})</span>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No results found. Try a different item.</p>
            )}
        </div>
    );
};

export default Results;