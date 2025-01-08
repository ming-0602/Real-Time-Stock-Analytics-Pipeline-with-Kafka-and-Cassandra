import React from 'react';
import CandlestickChart from './CandlestickChart';

function App() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-900">
            <div className="w-3/4 h-96">
                <CandlestickChart symbol="AAPL"/>
            </div>
        </div>


    );
}

export default App;