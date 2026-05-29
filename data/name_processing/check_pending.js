const sql = require('sql.js');
const fs = require('fs');

const dbPath = 'C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/ecomagent.db';
const dbBuffer = fs.readFileSync(dbPath);

sql().then(SQL => {
  const db = new SQL.Database(dbBuffer);
  
  // Check if short_name column exists
  const tableInfo = db.exec("PRAGMA table_info(products)");
  if (tableInfo.length > 0) {
    console.log("Table columns:", tableInfo[0].values.map(v => v[1]).join(", "));
  }
  
  // Count products without short_name
  try {
    const result = db.exec("SELECT COUNT(*) as count FROM products WHERE short_name IS NULL OR short_name = ''");
    if (result.length > 0) {
      console.log("Products without short_name:", result[0].values[0][0]);
    }
  } catch (e) {
    console.log("Error:", e.message);
  }
});
