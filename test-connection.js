const { sql, config } = require('./db.js');

async function testConnection() {
    try {
        console.log('Попытка подключения к SQL Server...');
        let pool = await sql.connect(config);
        
        // Проверяем подключение простым запросом
        const result = await pool.request().query('SELECT @@VERSION as version');
        console.log('SQL Server версия:', result.recordset[0].version);
        console.log('Подключение успешно установлено');
    } catch (err) {
        console.error('Детали ошибки:', err);
    } finally {
        await sql.close();
    }
}

testConnection(); 