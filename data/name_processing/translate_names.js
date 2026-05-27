// 商品名称翻译脚本
const fs = require('fs');
const path = require('path');

const INPUT_FILE = path.join(__dirname, 'all_items.json');
const OUTPUT_FILE = path.join(__dirname, 'processed_names.json');

// 翻译规则
function translateProductName(name) {
    if (!name || name.trim() === '') return '';
    
    name = name.trim();
    const lower = name.toLowerCase();
    
    // Apple 产品
    if (lower.match(/apple iphone (\d+)(?:\s+pro(?:\s+max)?)?/)) {
        const match = lower.match(/iphone (\d+)/);
        const model = match ? match[1] : '';
        if (lower.includes('pro max')) return `苹果iPhone ${model} Pro Max`;
        if (lower.includes('pro')) return `苹果iPhone ${model} Pro`;
        if (lower.includes('plus')) return `苹果iPhone ${model} Plus`;
        if (lower.includes('mini')) return `苹果iPhone ${model} Mini`;
        return `苹果iPhone ${model}`;
    }
    if (lower.includes('apple iphone se')) return '苹果iPhone SE';
    if (lower.includes('apple ipad')) return '苹果iPad';
    if (lower.includes('apple watch series')) {
        const match = lower.match(/series (\d+)/);
        return match ? `苹果Watch Series ${match[1]}` : '苹果Watch';
    }
    if (lower.includes('apple airpods pro')) {
        if (lower.includes('2nd')) return '苹果AirPods Pro 2代';
        return '苹果AirPods Pro';
    }
    if (lower.match(/apple airpods (\d)/)) {
        const match = lower.match(/airpods (\d)/);
        return match ? `苹果AirPods ${match[1]}` : '苹果AirPods';
    }
    if (lower.includes('apple airpods')) return '苹果AirPods';
    if (lower.includes('apple pencil')) return '苹果Pencil';
    
    // medicube 产品
    if (lower.includes('medicube')) {
        if (lower.includes('toner pads') || lower.includes('zero pore')) return 'Medicube零毛孔爽肤棉片';
        if (lower.includes('wrapping mask')) return 'Medicube胶原蛋白面膜';
        if (lower.includes('collagen jelly cream')) return 'Medicube胶原蛋白果冻霜';
        if (lower.includes('facial cleanser')) return 'Medicube洁面泡沫';
        if (lower.includes('pdrn')) return 'Medicube PDRN精华';
        return 'Medicube护肤产品';
    }
    
    // CeraVe 产品
    if (lower.includes('cerave')) {
        if (lower.includes('moisturizing cream')) return 'CeraVe保湿霜';
        if (lower.includes('hydrating facial cleanser')) return 'CeraVe洁面乳';
        if (lower.includes('cleanser')) return 'CeraVe洁面';
        return 'CeraVe护肤产品';
    }
    
    // Neutrogena 产品
    if (lower.includes('neutrogena')) {
        if (lower.includes('ultra sheer') || lower.includes('spf')) return '露得清防晒霜';
        if (lower.includes('makeup remover')) return '露得清卸妆湿巾';
        return '露得清护肤产品';
    }
    
    // The Ordinary 产品
    if (lower.includes('the ordinary')) {
        if (lower.includes('glycolic acid')) return 'The Ordinary甘醇酸爽肤水';
        if (lower.includes('hyaluronic acid')) return 'The Ordinary透明质酸精华';
        if (lower.includes('niacinamide')) return 'The Ordinary烟酰胺精华';
        return 'The Ordinary护肤产品';
    }
    
    // Amazon 设备
    if (lower.includes('amazon echo show')) {
        const match = lower.match(/echo show (\d+)/);
        return match ? `Amazon Echo Show ${match[1]}` : 'Amazon Echo Show';
    }
    if (lower.includes('amazon echo dot')) return 'Amazon Echo Dot';
    if (lower.includes('amazon echo spot')) return 'Amazon Echo Spot';
    if (lower.includes('amazon fire tv stick')) return 'Amazon Fire TV Stick';
    if (lower.includes('amazon fire hd')) return 'Amazon Fire HD平板';
    if (lower.includes('amazon kindle colorsoft')) return 'Kindle Colorsoft';
    if (lower.includes('amazon kindle paperwhite')) return 'Kindle Paperwhite';
    if (lower.includes('amazon basics')) {
        if (lower.includes('cotton swabs')) return 'Amazon Basics棉签';
        if (lower.includes('disinfecting wipes')) return 'Amazon Basics消毒湿巾';
        if (lower.includes('kitchen scale')) return 'Amazon Basics厨房秤';
        return 'Amazon Basics产品';
    }
    
    // Ring 设备
    if (lower.includes('ring')) {
        if (lower.includes('battery doorbell plus')) return 'Ring电池门铃Plus';
        if (lower.includes('battery doorbell')) return 'Ring电池门铃';
        if (lower.includes('wired doorbell pro')) return 'Ring有线门铃Pro';
        if (lower.includes('wired doorbell')) return 'Ring有线门铃';
        if (lower.includes('video doorbell')) return 'Ring可视门铃';
        if (lower.includes('indoor cam plus')) return 'Ring室内摄像头Plus';
        if (lower.includes('indoor cam')) return 'Ring室内摄像头';
        if (lower.includes('outdoor cam plus')) return 'Ring室外摄像头Plus';
        if (lower.includes('outdoor cam') || lower.includes('stick up cam')) return 'Ring室外摄像头';
        if (lower.includes('spotlight cam')) return 'Ring聚光摄像头';
        if (lower.includes('floodlight cam')) return 'Ring泛光摄像头';
        if (lower.includes('chime pro')) return 'Ring门铃提示器Pro';
        if (lower.includes('chime')) return 'Ring门铃提示器';
        if (lower.includes('solar panel')) return 'Ring太阳能板';
        if (lower.includes('battery pack')) return 'Ring电池包';
        return 'Ring智能家居产品';
    }
    
    // Blink 设备
    if (lower.includes('blink')) {
        if (lower.includes('outdoor 2k')) return 'Blink室外摄像头2K';
        if (lower.includes('outdoor') && lower.includes('floodlight')) return 'Blink泛光摄像头';
        if (lower.includes('outdoor')) return 'Blink室外摄像头';
        if (lower.includes('mini 2k')) return 'Blink Mini 2K';
        if (lower.includes('mini')) return 'Blink Mini';
        return 'Blink智能家居产品';
    }
    
    // 制冰机
    if (lower.includes('ice maker')) {
        if (lower.includes('nugget')) return '颗粒冰制冰机';
        if (lower.includes('countertop')) return '台式制冰机';
        return '制冰机';
    }
    
    // iPhone (非Apple前缀)
    if (lower.match(/iphone (\d+)(?:\s+pro(?:\s+max)?)?/)) {
        const match = lower.match(/iphone (\d+)/);
        const model = match ? match[1] : '';
        if (lower.includes('pro max')) return `iPhone ${model} Pro Max`;
        if (lower.includes('pro')) return `iPhone ${model} Pro`;
        if (lower.includes('plus')) return `iPhone ${model} Plus`;
        if (lower.includes('mini')) return `iPhone ${model} Mini`;
        return `iPhone ${model}`;
    }
    
    // AirPods
    if (lower.includes('airpods pro') && lower.includes('2nd')) return '苹果AirPods Pro 2代';
    if (lower.includes('airpods pro')) return '苹果AirPods Pro';
    if (lower.match(/airpods (\d)/)) {
        const match = lower.match(/airpods (\d)/);
        return match ? `苹果AirPods ${match[1]}` : '苹果AirPods';
    }
    
    // PlayStation
    if (lower.includes('playstation') || lower.includes('dualsense')) return 'PS5手柄';
    
    // Nintendo
    if (lower.includes('nintendo switch')) return '任天堂Switch';
    
    // Beats
    if (lower.includes('beats studio pro')) return 'Beats Studio Pro';
    if (lower.includes('beats solo')) return 'Beats Solo';
    
    // 知名品牌
    if (lower.includes('biodance')) return 'BIODANCE胶原蛋白面膜';
    if (lower.includes('eos') && lower.includes('body lotion')) return 'eos身体乳';
    if (lower.includes('mighty patch')) return 'Mighty Patch痘痘贴';
    if (lower.includes('panoxyl')) return 'PanOxyl祛痘洗面奶';
    if (lower.includes('nizoral')) return 'Nizoral去屑洗发水';
    if (lower.includes('aquaphor')) return 'Aquaphor修护膏';
    if (lower.includes('lodge') && lower.includes('cast iron')) return 'Lodge铸铁锅';
    if (lower.includes('crocs')) return 'Crocs洞洞鞋';
    if (lower.includes('duracell') && lower.includes('2032')) return '金霸王2032电池';
    if (lower.includes('ninja') && lower.includes('blender')) return 'Ninja搅拌机';
    if (lower.includes('ninja') && lower.includes('air fryer')) return 'Ninja空气炸锅';
    if (lower.includes('cosori') && lower.includes('air fryer')) return 'Cosori空气炸锅';
    if (lower.includes('kitchenaid')) return 'KitchenAid厨房工具';
    if (lower.includes('owala') && lower.includes('freesip')) return 'Owala FreeSip水杯';
    if (lower.includes('stanley') && lower.includes('quencher')) return 'STANLEY保温杯';
    if (lower.includes('yeti') && lower.includes('rambler')) return 'YETI保温杯';
    if (lower.includes('gorilla') && lower.includes('super glue')) return 'Gorilla强力胶';
    if (lower.includes('velcro')) return 'VELCRO魔术贴';
    if (lower.includes('tide') && lower.includes('detergent')) return '汰渍洗衣液';
    if (lower.includes('clorox') && lower.includes('wipes')) return '高乐氏消毒湿巾';
    if (lower.includes('lysol') && lower.includes('toilet')) return '来苏尔马桶清洁剂';
    if (lower.includes('band-aid')) return '邦迪创可贴';
    if (lower.includes('dove') && lower.includes('body wash')) return '多芬沐浴露';
    if (lower.includes('tree hut') && lower.includes('scrub')) return 'Tree Hut磨砂膏';
    if (lower.includes('silonn') && lower.includes('ice maker')) return 'Silonn制冰机';
    if (lower.includes('euhomy') && lower.includes('ice maker')) return 'EUHOMY制冰机';
    if (lower.includes('black+decker')) return 'Black+Decker电器';
    if (lower.includes('rubbermaid') && lower.includes('food storage')) return 'Rubbermaid食品收纳盒';
    if (lower.includes('hotor') && lower.includes('lunch')) return 'HOTOR保温饭盒';
    if (lower.includes('lifewit') && lower.includes('lunch')) return 'Lifewit午餐包';
    if (lower.includes('sensarte') && lower.includes('frying pan')) return 'SENSARTE不粘锅';
    if (lower.includes('reynolds') && lower.includes('parchment')) return 'Reynolds烘焙纸';
    
    // 通用产品类型识别
    if (lower.includes('sunscreen') || lower.includes('spf')) return '防晒产品';
    if (lower.includes('moisturizer') || lower.includes('lotion')) return '保湿产品';
    if (lower.includes('cleanser') || lower.includes('face wash')) return '洁面产品';
    if (lower.includes('serum')) return '精华产品';
    if (lower.includes('mask') && !lower.includes('oxygen')) return '面膜产品';
    if (lower.includes('shampoo')) return '洗发产品';
    if (lower.includes('conditioner')) return '护发产品';
    if (lower.includes('mascara')) return '睫毛膏';
    if (lower.includes('vitamin') || lower.includes('supplement')) return '保健品';
    if (lower.includes('protein')) return '蛋白产品';
    if (lower.includes('gloves')) return '手套';
    if (lower.includes('wipes')) return '湿巾';
    if (lower.includes('towel')) return '毛巾';
    if (lower.includes('blanket')) return '毯子';
    if (lower.includes('pillow')) return '枕头';
    if (lower.includes('chair')) return '椅子';
    if (lower.includes('table')) return '桌子';
    if (lower.includes('lamp') || lower.includes('light')) return '灯具';
    if (lower.includes('fan')) return '风扇';
    if (lower.includes('heater')) return '加热器';
    if (lower.includes('humidifier')) return '加湿器';
    if (lower.includes('air purifier')) return '空气净化器';
    if (lower.includes('vacuum')) return '吸尘器';
    if (lower.includes('mop')) return '拖把';
    if (lower.includes('scale')) return '秤';
    if (lower.includes('battery')) return '电池';
    if (lower.includes('cable') || lower.includes('cord')) return '数据线';
    if (lower.includes('charger')) return '充电器';
    if (lower.includes('case') && !lower.includes('pillow')) return '保护壳';
    if (lower.includes('screen protector')) return '屏幕保护膜';
    if (lower.includes('headphones') || lower.includes('earbuds') || lower.includes('earphones')) return '耳机';
    if (lower.includes('speaker')) return '音箱';
    if (lower.includes('camera')) return '相机';
    if (lower.includes('remote')) return '遥控器';
    if (lower.includes('controller')) return '游戏手柄';
    if (lower.includes('dog') || lower.includes('cat') || lower.includes('pet')) return '宠物用品';
    if (lower.includes('toy')) return '玩具';
    if (lower.includes('game')) return '游戏';
    if (lower.includes('book')) return '书籍';
    if (lower.includes('shoes') || lower.includes('sandals') || lower.includes('boots')) return '鞋类';
    if (lower.includes('shirt') || lower.includes('tee') || lower.includes('top')) return '上衣';
    if (lower.includes('pants') || lower.includes('jeans') || lower.includes('shorts')) return '裤子';
    if (lower.includes('dress') || lower.includes('skirt')) return '裙装';
    if (lower.includes('jacket') || lower.includes('coat')) return '外套';
    if (lower.includes('underwear') || lower.includes('bra')) return '内衣';
    if (lower.includes('bag') || lower.includes('backpack')) return '包袋';
    if (lower.includes('wallet')) return '钱包';
    if (lower.includes('watch') && !lower.includes('apple')) return '手表';
    if (lower.includes('sunglasses') || lower.includes('glasses')) return '眼镜';
    if (lower.includes('hat') || lower.includes('cap')) return '帽子';
    
    // 截断过长的名称
    if (name.length > 15) return name.substring(0, 15) + '...';
    return name;
}

// 主处理逻辑
console.log('读取商品数据...');
const items = JSON.parse(fs.readFileSync(INPUT_FILE, 'utf8'));
console.log(`共 ${items.length} 个商品`);

const results = [];
let count = 0;

for (const item of items) {
    count++;
    const shortName = translateProductName(item.name);
    
    results.push({
        id: item.id,
        short_name: shortName
    });
    
    if (count % 500 === 0) {
        console.log(`已处理: ${count} / ${items.length}`);
    }
}

// 输出结果
const output = {
    batch_id: `translate_${new Date().toISOString().replace(/[-:T]/g, '').substring(0, 15)}`,
    items: results
};

console.log('保存结果...');
fs.writeFileSync(OUTPUT_FILE, JSON.stringify(output, null, 2), 'utf8');
console.log(`完成！结果已保存到: ${OUTPUT_FILE}`);
