const fs = require('fs');
const path = require('path');

// 读取输入文件
const inputFile = path.join(__dirname, 'all_items.json');
const outputFile = path.join(__dirname, 'processed_names.json');

const data = JSON.parse(fs.readFileSync(inputFile, 'utf-8'));

// 翻译函数
function translateName(name) {
  if (!name || name.trim() === '') return '未知商品';
  
  name = name.trim();
  
  // 特殊处理
  const specialCases = {
    'essence': 'essence精华',
    'Hibiclens': 'Hibiclens消毒液',
    'Grad Cap Remix': '毕业帽装饰',
    'blink plus plan with monthly auto-renewal': 'Blink Plus月度订阅',
    'blink plus ai plan with monthly auto-renewal': 'Blink AI月度订阅',
    'Alexa Emergency Assist Monthly (auto-renewal)': 'Alexa紧急协助订阅',
  };
  
  if (specialCases[name]) return specialCases[name];
  
  // 知名品牌（保留英文）
  const brands = [
    'Apple', 'Samsung', 'Amazon Basics', 'Amazon Essentials', 'Amazon', 'Google', 'Microsoft', 'Sony', 'Nike', 
    'Adidas', 'Crocs', 'medicube', 'BIODANCE', 'eos', 'Neutrogena', 'Maybelline', 'CeraVe', 'The Ordinary', 
    'PanOxyl', 'EltaMD', 'Paula\'s Choice', 'Aquaphor', 'Vanicream', 'Illiyoon', 'Tree Hut', 'Mighty Patch', 
    'Nizoral', 'Dove', 'Hanes', 'Gildan', 'Carhartt', 'Comfort Colors', 'Dickies', 'New Balance', 'Skechers', 
    'Fruit of the Loom', 'Blink', 'Ring', 'Anker', 'Soundcore', 'JBL', 'Beats', 'SHOKZ', 'JLab', 'TAGRY', 
    'Oura', 'Roku', 'Bounty', 'Scott', 'Charmin', 'Angel Soft', 'Quilted Northern', 'Cottonelle', 'Dawn', 
    'Tide', 'Clorox', 'Lysol', 'Duracell', 'Energizer', 'Band-Aid', 'Ninja', 'KitchenAid', 'Lodge', 'Cosori', 
    'Rubbermaid', 'STANLEY', 'Owala', 'YETI', 'HydroJug', 'Etekcity', 'Quest', 'Optimum Nutrition', 
    'Vital Proteins', 'LMNT', 'Liquid I.V.', 'Nordic Naturals', 'Pure Encapsulations', 'GE', 'Gorilla', 
    'Loctite', 'Velcro', 'O-Cedar', 'Puracy', 'Hibiclens', 'Affresh', 'Kodak', 'Playstation', 'BrüMate', 
    'REDUCE', 'Sok It', 'Lifewit', 'HOTOR', 'SENSARTE', 'SUNLU', 'MedPride', 'Schneider', 'Supmedic', 'DIYMAG', 
    'Life360', 'Tile', 'Sylvania', 'Nutrafol', 'Revlon', 'Laura Geller', 'e.l.f.', 'Dr.Melaxin', 'Dr.Althea', 
    'Salt & Stone', 'Naturium', 'EQQUALBERRY', 'VALITIC', 'Clean Skin Club', 'Julep', 'grace & stella', 
    'Body Restore', 'Nippies', 'EverFoams', 'KuaiLu', 'ANRABESS', 'SHAPERMINT', 'Wrangler', 'Rustler', 
    'J.VER', 'COOFANDY', 'OEAK', 'LetsJoli', 'OFEEFAN', 'COCOMARTS', 'Vertvie', 'YEOREO', 'G4Free', 
    'FITRELL', 'REPEL', 'wernies', 'Chantomoo', 'GIURKUU', 'Hstyle', 'Socomi', 'AceThrills', 'OEAGO', 
    'ukeetap', 'SURETIVIAN', 'Zeawec', 'DOQAUS', 'TempPro', 'Alpha Grillers', 'Fullstar', 'Mueller', 
    'bmani', 'TESSAN', 'Alex Tech', 'JohnBee', 'JOYMOOP', 'Molly\'s Suds', 'LIFARA', 'Art3d', 'Litepak', 
    'Swihauk', 'Borje', 'NNPCBT', 'travel inspira', 'Dash', 'bella', 'TrendPlain', 'Homaxy', 'S&T INC.', 
    'Inspire', 'Pure Protein', 'Ultima Replenisher', 'Physician\'s CHOICE', 'Depend', 'LUMIFY', 'O Positiv', 
    'Cozy Essential', 'Miss Mouth\'s', 'Grandma\'s Secret', '30 SECONDS', 'Unboxme', 'Sampeel', 'Zeagoo', 
    'CHICME', 'Trendy Queen', 'IECCP', 'DUDE Wipes', 'MRS. MEYER\'S', 'La Roche-Posay', 'FUJIFILM', 'Instax',
  ];
  
  // 产品类型映射（优先级从高到低）
  const productTypes = [
    // 护肤美妆（精确匹配）
    ['Toner Pads', '爽肤水棉片'], ['Zero Pore Pad', '零毛孔棉片'], ['Bio-Collagen Real Deep Mask', '生物胶原面膜'],
    ['Collagen Overnight Peel Off', '胶原过夜面膜'], ['PDRN Pink Peptide Serum', 'PDRN精华'],
    ['Exosome Shot', '外泌体精华'], ['Glycolic Acid 7%', '甘醇酸7%'], ['Niacinamide 10%', '烟酰胺10%'],
    ['Hyaluronic Acid 2%', '透明质酸2%'], ['SKIN PERFECTING 2% BHA', 'BHA爽肤水'],
    ['Body Lotion', '身体乳'], ['Cotton Swabs', '棉签'], ['Sunscreen Lotion', '防晒乳'],
    ['Sunscreen', '防晒霜'], ['Makeup Remover Wipes', '卸妆湿巾'], ['Wrapping Mask', '包裹面膜'],
    ['Jelly Cream', '果冻霜'], ['Mascara', '睫毛膏'], ['Clean Towels', '洁面巾'],
    ['Hand Soap Refill', '洗手液补充装'], ['Hand Soap', '洗手液'], ['Exfoliating Toner', '去角质爽肤水'],
    ['Body Wash', '沐浴露'], ['Under Eye Mask', '眼膜'], ['Acne Foaming Wash', '祛痘洁面乳'],
    ['Shower Steamers', '淋浴香薰'], ['Anti-Dandruff Shampoo', '去屑洗发水'], ['Shampoo', '洗发水'],
    ['Cotton Rounds', '化妆棉'], ['Sugar Scrub', '糖磨砂'], ['Face Sunscreen', '面部防晒'],
    ['Illuminating Serum', '提亮精华'], ['Serum', '精华'], ['Healing Ointment', '修复膏'],
    ['Face Moisturizer', '面部保湿霜'], ['Moisturizing Cream', '保湿霜'], ['Moisturizing Lotion', '保湿乳'],
    ['Moisturizer', '保湿霜'], ['Eyeliner', '眼线笔'], ['Facial Cleanser', '洁面乳'],
    ['Cleansing Foam', '洁面泡沫'], ['Eyeshadow', '眼影'], ['Shadow Stick', '眼影棒'],
    ['Balm Stick', '膏棒'], ['Deodorant', '除臭剂'], ['Brow Pencil', '眉笔'],
    ['Hair Growth Supplements', '生发补充剂'], ['Soap Bars', '肥皂'], ['Capsule Cream', '胶囊霜'],
    ['Relief Cream', '舒缓霜'], ['Dark Spot Remover', '祛斑'], ['Ceramide Ato Concentrate Cream', '神经酰胺霜'],
    ['Double Repair', '双重修复'], ['Ultra Sheer Dry-Touch', '干爽触感'], ['Micellar', '微胶束'],
    ['Collagen Jelly Cream', '胶原果冻霜'], ['Zero Pore Capsule', '零毛孔胶囊'],
    
    // 电子产品（精确匹配）
    ['EarPods Headphones', 'EarPods耳机'], ['AirTag', 'AirTag追踪器'], ['Wireless Earbuds', '无线耳机'],
    ['Echo Dot Max', 'Echo Dot Max'], ['Echo Dot Kids', 'Echo Dot儿童版'], ['Echo Dot', 'Echo Dot'],
    ['Kindle Paperwhite Signature Edition', 'Kindle签名版'], ['Kindle Paperwhite', 'Kindle Paperwhite'],
    ['Kindle Colorsoft', 'Kindle Colorsoft'], ['Kindle', 'Kindle'], ['Streaming Stick 4K', '4K流媒体棒'],
    ['Streaming Stick HD', '高清流媒体棒'], ['Apple Watch Series', 'Apple Watch'], ['Apple Watch', 'Apple Watch'],
    ['Wall Charger', '充电器'], ['Surge Protector Power Strip', '浪涌保护排插'], ['Surge Protector', '浪涌保护器'],
    ['Power Strip', '排插'], ['Extension Cord', '延长线'], ['Remote Control', '遥控器'],
    ['Instant Film', '胶片'], ['Sizing Kit', '尺寸套装'], ['Zip Ties', '扎带'],
    ['Fire TV Stick 4K Max', 'Fire TV 4K Max'], ['Fire TV Stick 4K Plus', 'Fire TV 4K Plus'],
    ['Fire TV Stick 4K Select', 'Fire TV 4K'], ['Fire TV Stick 4K', 'Fire TV 4K'], 
    ['Fire TV Stick HD', 'Fire TV HD'], ['Echo Show 15', 'Echo Show 15'], ['Echo Show 11', 'Echo Show 11'],
    ['Echo Show 5', 'Echo Show 5'], ['Echo Show', 'Echo Show'], ['Echo Spot', 'Echo Spot'],
    ['Noise Cancelling Earbuds', '降噪耳机'], ['Portable Bluetooth Speaker', '便携蓝牙音箱'],
    ['Bluetooth Speaker', '蓝牙音箱'], ['Bone Conduction Headphones', '骨传导耳机'],
    ['Video Doorbell Wired', '有线视频门铃'], ['Video Doorbell', '视频门铃'], ['Doorbell', '门铃'],
    ['Indoor Cam Plus', '室内摄像头Plus'], ['Indoor Cam', '室内摄像头'], ['Outdoor Cam Plus', '户外摄像头Plus'],
    ['Outdoor Cam', '户外摄像头'], ['Stick Up Cam', '摄像头'], ['Chime Pro', '门铃提示器Pro'],
    ['Chime', '门铃提示器'], ['mesh wifi add-on extender', 'Mesh WiFi扩展器'], ['Battery Pack', '电池组'],
    ['Solar Panel', '太阳能板'], ['Floodlight Cam Wired Pro', '泛光灯Pro'], ['Floodlight Cam Wired Plus', '泛光灯Plus'],
    ['Floodlight Cam', '泛光灯摄像头'], ['Spotlight Cam Plus', '聚光灯摄像头'], ['Pan-Tilt Indoor Cam', '云台室内摄像头'],
    ['Smart Plug', '智能插座'], ['Adjustable Stand', '可调节支架'], ['Emergency Assist', '紧急协助'],
    ['DualSense Wireless Controller', 'DualSense手柄'], ['Light Bulb', '灯泡'], ['LED 4K UHD', 'LED 4K超高清'],
    ['Smart Fire TV', '智能Fire TV'], ['eero 6', 'eero 6'], ['Plant-Based Leather Case', '植物皮革保护套'],
    ['AirPods Pro', 'AirPods Pro'], ['AirPods', 'AirPods'], ['iPad', 'iPad'], ['iPhone', 'iPhone'],
    ['MacBook', 'MacBook'], ['Laptop', '笔记本'], ['Digital Camera', '数码相机'],
    
    // 服装（精确匹配）
    ['Boxer Briefs', '平角内裤'], ['Wide Leg Pants', '阔腿裤'], ['Flowy Palazzo', '飘逸阔腿裤'],
    ['Wireless Bra', '无钢圈文胸'], ['Jelly Bra', '果冻文胸'], ['Strapless Bra', '无肩带文胸'],
    ['Dress Shirts', '正装衬衫'], ['Linen Shirts', '亚麻衬衫'], ['Pocket T-Shirt', '口袋T恤'],
    ['Heavyweight Short Sleeve Tee', '重磅短袖T恤'], ['Beefy-t T-Shirt', '重磅T恤'], ['Ultra Cotton T-Shirt', '精梳棉T恤'],
    ['Crew T-Shirts', '圆领T恤'], ['Sleeveless Tag Free', '无袖无标'], ['Crew Tee Undershirts', '圆领汗衫'],
    ['Nipple Covers', '乳贴'], ['Memory Foam House Slippers', '记忆棉拖鞋'], ['Open-toe Slippers', '露趾拖鞋'],
    ['Fuzzy Slippers', '毛绒拖鞋'], ['Classic Clog', '经典洞洞鞋'], ['Flip Flops', '人字拖'],
    ['Arch Support', '足弓支撑'], ['Henley Tops', '亨利领上衣'], ['Cotton Bikini', '棉质比基尼'],
    ['No Underwire', '无钢圈'], ['Plus Size Minimizer', '大码缩胸文胸'], ['Plus Size', '大码'],
    ['Cargo Stretch Short', '工装短裤'], ['Tank Tops', '背心'], ['Built-in Bra Tank Tops', '内置文胸背心'],
    ['V Neck Ribbed Knit', 'V领罗纹'], ['No Show Socks', '隐形袜'], ['Low Socks', '低帮袜'],
    ['Ruffle Socks', '荷叶边袜'], ['Crew Socks', '中筒袜'], ['Compression Socks', '压缩袜'],
    ['Graduation Cap Headband', '毕业帽发箍'], ['Yoga Pants', '瑜伽裤'], ['Workout Leggings', '运动打底裤'],
    ['Leggings', '打底裤'], ['No Front Seam', '无前缝'], ['Water Shoes', '涉水鞋'],
    ['Quick-Dry Aqua Socks', '速干水鞋'], ['Sock Shoes', '袜鞋'], ['Toddler Walking Shoes', '学步鞋'],
    ['Golf Pants', '高尔夫裤'], ['Stretch Work Dress Pants', '弹力正装裤'], ['Cross Trainer', '综合训练鞋'],
    ['Go Walk Flex', 'Go Walk Flex'], ['Shapewear', '塑身衣'], ['Kimono Cardigan', '和服开衫'],
    ['Floral Print Puff Sleeve', '花卉泡泡袖'], ['3/4 Length Sleeve', '七分袖'],
    ['Short Sleeve Tops', '短袖上衣'], ['Short Sleeve Shirts', '短袖衬衫'], ['Short Sleeve', '短袖'],
    ['Long Sleeve', '长袖'], ['Sleeveless', '无袖'], ['Classic Relaxed Fit', '经典宽松版'],
    ['Relaxed Fit', '宽松版'], ['Regular-Fit', '常规版'], ['Classic Cargo', '经典工装'],
    
    // 日用品（精确匹配）
    ['Quick Size Paper Towels', '快速抽取纸巾'], ['Pick-A-Size Paper Towels', '自选尺寸纸巾'],
    ['Select-A-Size Paper Towels', '自选尺寸纸巾'], ['Tear-A-Square Paper Towels', '可撕方块纸巾'],
    ['Flex-Sheets Paper Towels', '弹性纸巾'], ['Paper Towels', '纸巾'], ['Ultra Soft Toilet Paper', '超柔卫生纸'],
    ['Ultra Strong Toilet Paper', '超韧卫生纸'], ['Ultra Plush Toilet Paper', '超蓬松卫生纸'],
    ['Ultra Clean Toilet Paper', '超洁净卫生纸'], ['Ultra Comfort Toilet Paper', '超舒适卫生纸'],
    ['2-Ply Soft Toilet Paper', '双层柔卫生纸'], ['2-Ply Toilet Paper', '双层卫生纸'],
    ['3-Ply Paper Towels', '三层纸巾'], ['Toilet Paper', '卫生纸'], ['Flushable Wipes', '可冲湿巾'],
    ['Wet Wipes', '湿巾'], ['AA Alkaline Batteries', 'AA碱性电池'], ['AAA Batteries', 'AAA电池'],
    ['Alkaline Batteries', '碱性电池'], ['Lithium Battery', '锂电池'], ['Disposable Paper Plates', '一次性纸盘'],
    ['Paper Plates', '纸盘'], ['Electrolytes', '电解质'], ['Electrolyte Powder', '电解质粉'],
    ['Zero Sugar Electrolytes', '零糖电解质'], ['Hydration Multiplier', '补水倍增剂'], ['Sugar-Free', '无糖'],
    ['Creatine Monohydrate Powder', '一水肌酸粉'], ['Whey Protein Powder', '乳清蛋白粉'], ['Protein Powder', '蛋白粉'],
    ['Protein Bars', '蛋白棒'], ['Collagen Peptides Powder', '胶原蛋白粉'], ['Dish Soap Refill', '洗洁精补充装'],
    ['Dish Soap', '洗洁精'], ['Kitchen Drawstring Trash Bags', '厨房垃圾袋'], ['Drawstring Trash Bags', '抽绳垃圾袋'],
    ['Trash Bags', '垃圾袋'], ['Sterile Alcohol Prep Pads', '无菌酒精棉片'], ['Alcohol Prep Pads', '酒精棉片'],
    ['Probiotics', '益生菌'], ['Adhesive Bandages', '创可贴'], ['Adult Diapers', '成人纸尿裤'],
    ['Eye Drops', '眼药水'], ['Disinfecting Wipes', '消毒湿巾'], ['Toilet Bowl Cleaner', '马桶清洁剂'],
    ['Laundry Detergent', '洗衣液'], ['PODS', '洗衣凝珠'], ['Nitrile Exam Gloves', '丁腈检查手套'],
    ['Nitrile Disposable Gloves', '丁腈手套'], ['Disposable Gloves', '一次性手套'], ['Disposable Face Mask', '一次性口罩'],
    ['Face Mask', '口罩'], ['Vacuum Storage Bags', '真空收纳袋'], ['Super Glue Gel', '强力胶凝胶'],
    ['Super Glue', '强力胶'], ['Dishwasher Pods', '洗碗机凝珠'], ['3D Printer Filament', '3D打印耗材'],
    ['Magnetic Hooks', '磁性挂钩'], ['Lint Rollers', '粘毛滚筒'], ['Spin Mop', '旋转拖把'],
    ['Hydrocolloid Roll', '水胶体卷'], ['Silicone Caulk', '硅胶填缝剂'], ['Isopropyl Alcohol', '异丙醇酒精'],
    ['Hand Towel', '擦手纸'], ['Stain Remover', '去渍剂'], ['Mold Remover', '霉菌去除剂'],
    ['Magnesium', '镁补充剂'], ['Fluoride Free Toothpaste', '无氟牙膏'], ['Toothpaste', '牙膏'],
    ['Hook and Loop Tape', '魔术贴'], ['Coffee Syrup Pump', '咖啡糖浆泵'],
    
    // 厨房用品（精确匹配）
    ['Insulated Stainless Steel Water', '保温水杯'], ['Insulated Stainless Steel', '保温杯'],
    ['Tumbler with Handle and Straw', '带手柄吸管杯'], ['Tumbler', '随行杯'], ['Water Bottle', '水杯'],
    ['Traveler', '旅行杯'], ['Rambler', '随行杯'], ['Quencher', 'Quencher杯'], ['FreeSip', 'FreeSip杯'],
    ['SmoothSip', 'SmoothSip杯'], ['JavaSok', 'JavaSok杯'], ['Era', 'Era杯'], ['Sway', 'Sway杯'],
    ['Saltini', 'Saltini杯'], ['Digital Kitchen Scale', '电子厨房秤'], ['Food Kitchen Scale', '厨房秤'],
    ['Instant Read Meat Thermometer', '即时读数温度计'], ['Meat Thermometer', '肉类温度计'],
    ['All Purpose Kitchen Shears', '多用途厨房剪刀'], ['Kitchen Shears', '厨房剪刀'],
    ['Multifunction Can Opener', '多功能开罐器'], ['Can Opener', '开罐器'],
    ['Cotton Waffle Weave Kitchen Dish Cloths', '棉质洗碗布'], ['Dish Cloths', '洗碗布'],
    ['Air Fryer Paper Liners', '炸锅纸'], ['Parchment Paper', '羊皮纸'], ['Sponge Holder', '海绵架'],
    ['Compact Personal Blender', '个人搅拌机'], ['Professional Plus Blender', '专业搅拌机'], ['Blender', '搅拌机'],
    ['Vegetable Chopper', '切菜器'], ['Pro Chopper', '专业切菜器'], ['Mandoline', '切片器'],
    ['Dish Drying Mat', '晾干垫'], ['Insulated Lunch Box', '保温饭盒'], ['Lunch Bag', '午餐包'], ['Lunch Box', '饭盒'],
    ['Rapid Egg Cooker', '快速煮蛋器'], ['Expandable Silverware Organizer', '可扩展餐具收纳盒'],
    ['Silverware Organizer', '餐具收纳盒'], ['Seasoned Cast Iron Skillet', '铸铁平底锅'], ['Cast Iron Skillet', '铸铁锅'],
    ['Ice Cube Tray with Lid and Bin', '冰格套装'], ['Ice Cube Tray', '冰格'],
    ['Electric Salt and Pepper Grinder Set', '电动盐胡椒研磨器'], ['Salt and Pepper Grinder', '盐胡椒研磨器'],
    ['TurboBlaze Air Fryer', 'TurboBlaze炸锅'], ['Air Fryer', '空气炸锅'], ['Chicken Shredder', '鸡肉撕碎器'],
    ['Glass Food Storage Containers', '玻璃食品盒'], ['Plastic Food Storage', '塑料食品盒'],
    ['Food Storage Containers', '食品储存盒'], ['Bamboo Cutting Board', '竹砧板'], ['Cutting Board', '砧板'],
    ['Nonstick Frying Pan', '不粘煎锅'], ['Frying Pan', '煎锅'], ['Skillet', '平底锅'],
    ['Meat Chopper', '碎肉器'], ['Tongs For Cooking', '烹饪夹'], ['Tongs', '夹子'],
    ['2 Slice Slim Toaster', '两片超薄烤面包机'],
    
    // 其他
    ['Mothers Day Gifts', '母亲节礼物'], ['Gifts for Mom', '妈妈礼物'], ['Gifts for Grandma', '奶奶礼物'],
    ['Mothers Day', '母亲节'], ['Valentines', '情人节'], ['Luggage Scale', '行李秤'],
    ['Windproof Travel Umbrella', '防风旅行伞'], ['Umbrella', '雨伞'], ['Grad Cap', '毕业帽'],
  ];
  
  // 提取品牌
  let brand = '';
  let remaining = name;
  
  for (const b of brands) {
    if (name.toLowerCase().startsWith(b.toLowerCase())) {
      brand = b;
      remaining = name.substring(b.length).trim();
      break;
    }
  }
  
  // 提取产品类型
  let productType = '';
  for (const [pattern, translation] of productTypes) {
    if (remaining.toLowerCase().includes(pattern.toLowerCase())) {
      productType = translation;
      break;
    }
  }
  
  // 如果没有匹配到产品类型，尝试从整个名称匹配
  if (!productType) {
    for (const [pattern, translation] of productTypes) {
      if (name.toLowerCase().includes(pattern.toLowerCase())) {
        productType = translation;
        break;
      }
    }
  }
  
  // 如果还是没有，提取关键词
  if (!productType) {
    const keywords = remaining.split(/\s+/).filter(w => w.length > 2).slice(0, 2);
    productType = keywords.join(' ') || remaining.split(/\s+/)[0] || '';
  }
  
  // 品牌缩写映射（长品牌名缩短）
  const brandShortcuts = {
    'Amazon Basics': '亚马逊',
    'Amazon Essentials': '亚马逊',
    'Amazon': '亚马逊',
    'Mighty Patch': '祛痘贴',
    'Clean Skin Club': '洁面巾',
    'Laura Geller': 'Laura',
    'MRS. MEYER\'S': 'Meyer',
    'MRS. MEYER\'S CLEAN DAY': 'Meyer',
    'grace & stella': 'G&S',
    'Body Restore': '香薰',
    'Paula\'s Choice': 'Paula',
    'The Ordinary': 'TO',
    'Physician\'s CHOICE': 'PC',
    'Grandma\'s Secret': 'Grandma',
    'Miss Mouth\'s': 'MissM',
    'Fruit of the Loom': 'FOTL',
    'Optimum Nutrition': 'ON',
    'Pure Encapsulations': 'PE',
    'Nordic Naturals': 'NN',
    'Liquid I.V.': 'LIV',
    'Vital Proteins': 'VP',
    'Quilted Northern': 'QN',
    'Angel Soft': 'AS',
    'Cottonelle': 'Cott',
  };
  
  // 缩短品牌名
  const displayBrand = brandShortcuts[brand] || brand;
  
  // 构建短名称
  let shortName = (displayBrand ? displayBrand + ' ' : '') + productType;
  
  // 提取型号/版本
  const versionPatterns = [
    /(\d+)(?:st|nd|rd|th)?\s*(?:Gen|Generation)/i,
    /Series\s*(\d+)/i,
    /(\d+)(?:th)?\s*Gen/i,
    /(\d+\.\d+)/,  // 版本号如 2.0
  ];
  
  for (const vp of versionPatterns) {
    const match = name.match(vp);
    if (match) {
      shortName += ' ' + match[1] + '代';
      break;
    }
  }
  
  // 清理并限制长度（中文按1.5字符计算，英文算1）
  shortName = shortName.trim();
  
  // 计算显示长度（中文算1.5，英文算1）
  const displayLen = (str) => {
    let len = 0;
    for (const c of str) {
      len += c.charCodeAt(0) > 127 ? 1.5 : 1;
    }
    return len;
  };
  
  // 限制在22个显示字符内（约等于15个中文字符的视觉效果）
  while (displayLen(shortName) > 22 && shortName.length > 0) {
    shortName = shortName.substring(0, shortName.length - 1);
  }
  shortName = shortName.trim();
  
  // 确保有效
  if (shortName.length < 2) {
    shortName = name.split(/\s+/).slice(0, 2).join(' ').substring(0, 15);
  }
  
  return shortName || '未知商品';
}

// 处理所有商品
const result = {
  batch_id: "ecomagent-translate-names-20260528",
  items: data.map(item => ({
    id: item.id,
    short_name: translateName(item.name)
  }))
};

// 写入输出文件
fs.writeFileSync(outputFile, JSON.stringify(result, null, 2), 'utf-8');

console.log(`处理完成: ${result.items.length} 条数据已保存到 ${outputFile}`);