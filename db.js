const sql = require('mssql/msnodesqlv8');

const config = {
    driver: 'msnodesqlv8',
    connectionString: 'Driver={SQL Server Native Client 11.0};Server=(localdb)\\SQLEXPRESS;Database=FaceRecognitionDB;Trusted_Connection=yes;',
    options: {
        trustServerCertificate: true,
        trustedConnection: true
    }
};

async function connectDB() {
    try {
        await sql.connect(config);
        console.log('Connected to SQL Server');
    } catch (err) {
        console.error('Database connection failed:', err);
        throw err;
    }
}

module.exports = {
    connectDB,
    sql,
    config
}; 