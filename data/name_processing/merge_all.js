const fs = require('fs');
const path = require('path');

const translatedDir = 'C:\\Users\\Etroi\\.openclaw\\workspace\\code\\EcomAgent\\data\\name_processing\\translated';
const outputPath = 'C:\\Users\\Etroi\\.openclaw\\workspace\\code\\EcomAgent\\data\\name_processing\\processed_names.json';

const allItems = [];
const batchFiles = fs.readdirSync(translatedDir)
  .filter(f => f.startsWith('batch_') && f.endsWith('.json'))
  .sort((a, b) => {
    const numA = parseInt(a.match(/batch_(\d+)/)[1]);
    const numB = parseInt(b.match(/batch_(\d+)/)[1]);
    return numA - numB;
  });

batchFiles.forEach(file => {
  const content = JSON.parse(fs.readFileSync(path.join(translatedDir, file), 'utf8'));
  if (content.items) {
    content.items.forEach(item => {
      allItems.push({
        id: item.id,
        short_name: item.short_name
      });
    });
  }
});

const result = {
  batch_id: 'merged_all_batches',
  items: allItems
};

fs.writeFileSync(outputPath, JSON.stringify(result, null, 2), 'utf8');
console.log('Merged ' + allItems.length + ' items to ' + outputPath);
