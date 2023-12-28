import React, { useState, useEffect } from 'react';
import { Select, MenuItem, FormControl, List, ListItem, SelectChangeEvent } from '@mui/material';

interface Product {
    kandidat: string;
    kurzbezeichnung: string; // or Date if your timestamps are Date objects
}

const ProductList = () => {
    const [products, setProducts] = useState<Product[]>([]);
    const [selectedProductId, setSelectedProductId] = useState('');

    // Fetch data from the server
    useEffect(() => {
        fetch('http://localhost:8000/wahlkreis/q2')
            .then(response => response.json())
            .then(data => setProducts(data))
            .catch(error => console.error('There was an error fetching the data', error));
    }, []);

    // Extract distinct product IDs
    const productIds = Array.from(new Set(products.map(product => product.kurzbezeichnung)));

    // Handle selection change
    const handleSelectionChange = (event: SelectChangeEvent<string>) => {
        setSelectedProductId(event.target.value as string);
    };

    // Filter timestamps for selected product ID
    const filteredTimestamps = products.filter(product => product.kurzbezeichnung === selectedProductId);

    return (
        <div>
            <FormControl fullWidth>
                <Select
                    value={selectedProductId}
                    onChange={handleSelectionChange}
                    displayEmpty
                    inputProps={{ 'aria-label': 'Without label' }}
                >
                    <MenuItem value="" disabled>
                        Select a Product ID
                    </MenuItem>
                    {productIds.map(id => (
                        <MenuItem key={id} value={id}>{id}</MenuItem>
                    ))}
                </Select>
            </FormControl>
            <List>
                {filteredTimestamps.map((product, index) => (
                    <ListItem key={index}>{product.kandidat}</ListItem>
                ))}
            </List>
        </div>
    );
};

export default ProductList;