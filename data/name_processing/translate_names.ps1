# 商品名称批量翻译脚本
$INPUT_FILE = "C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\all_items.json"
$OUTPUT_FILE = "C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json"

# 翻译函数 - 基于规则的智能翻译
function Translate-ProductName {
    param([string]$name)
    
    if ([string]::IsNullOrWhiteSpace($name)) { return "" }
    
    $name = $name.Trim()
    $lower = $name.ToLower()
    
    # 特殊模式匹配
    
    # Apple 产品
    if ($lower -match "apple iphone (\d+)(?:\s+pro(?:\s+max)?)?") {
        $model = $Matches[1]
        if ($lower -match "pro max") { return "苹果iPhone $model Pro Max" }
        if ($lower -match "pro") { return "苹果iPhone $model Pro" }
        if ($lower -match "plus") { return "苹果iPhone $model Plus" }
        if ($lower -match "mini") { return "苹果iPhone $model Mini" }
        return "苹果iPhone $model"
    }
    if ($lower -match "apple iphone se") { return "苹果iPhone SE" }
    if ($lower -match "apple ipad") { return "苹果iPad" }
    if ($lower -match "apple watch series (\d+)") { return "苹果Watch Series $($Matches[1])" }
    if ($lower -match "apple airpods pro") { return "苹果AirPods Pro" }
    if ($lower -match "apple airpods (\d+)") { return "苹果AirPods $($Matches[1])" }
    if ($lower -match "apple airpods") { return "苹果AirPods" }
    
    # medicube 产品
    if ($lower -match "medicube") {
        if ($lower -match "toner pads.*2\.0") { return "Medicube零毛孔爽肤棉片2.0" }
        if ($lower -match "wrapping mask") { return "Medicube胶原蛋白过夜面膜" }
        if ($lower -match "collagen jelly cream") { return "Medicube胶原蛋白果冻霜" }
        if ($lower -match "facial cleanser") { return "Medicube零毛孔洁面泡沫" }
        if ($lower -match "pdrn.*serum") { return "Medicube PDRN精华" }
        if ($lower -match "capsule cream.*vitamin c") { return "Medicube维C胶囊霜" }
        if ($lower -match "exosome") { return "Medicube外泌体精华" }
        return "Medicube护肤产品"
    }
    
    # CeraVe 产品
    if ($lower -match "cerave") {
        if ($lower -match "moisturizing cream") { return "CeraVe保湿霜" }
        if ($lower -match "moisturizing lotion") { return "CeraVe保湿乳液" }
        if ($lower -match "hydrating facial cleanser") { return "CeraVe洁面乳" }
        if ($lower -match "cleanser") { return "CeraVe洁面" }
        return "CeraVe护肤产品"
    }
    
    # Neutrogena 产品
    if ($lower -match "neutrogena") {
        if ($lower -match "ultra sheer.*spf") { return "露得清防晒霜SPF70" }
        if ($lower -match "makeup remover wipes") { return "露得清卸妆湿巾" }
        return "露得清护肤产品"
    }
    
    # The Ordinary 产品
    if ($lower -match "the ordinary") {
        if ($lower -match "glycolic acid") { return "The Ordinary甘醇酸爽肤水" }
        if ($lower -match "hyaluronic acid") { return "The Ordinary透明质酸精华" }
        if ($lower -match "niacinamide") { return "The Ordinary烟酰胺精华" }
        return "The Ordinary护肤产品"
    }
    
    # Amazon 设备
    if ($lower -match "amazon echo show (\d+)") { return "Amazon Echo Show $($Matches[1])" }
    if ($lower -match "amazon echo dot") { return "Amazon Echo Dot" }
    if ($lower -match "amazon echo spot") { return "Amazon Echo Spot" }
    if ($lower -match "amazon fire tv stick") { return "Amazon Fire TV Stick" }
    if ($lower -match "amazon fire hd (\d+)") { return "Amazon Fire HD $($Matches[1])平板" }
    if ($lower -match "amazon kindle colorsoft") { return "Kindle Colorsoft" }
    if ($lower -match "amazon kindle paperwhite") { return "Kindle Paperwhite" }
    if ($lower -match "amazon basics") {
        if ($lower -match "cotton swabs") { return "Amazon Basics棉签" }
        if ($lower -match "cotton rounds") { return "Amazon Basics化妆棉" }
        if ($lower -match "disinfecting wipes") { return "Amazon Basics消毒湿巾" }
        if ($lower -match "kitchen scale") { return "Amazon Basics厨房秤" }
        return "Amazon Basics产品"
    }
    
    # Ring 设备
    if ($lower -match "ring") {
        if ($lower -match "battery doorbell plus") { return "Ring电池门铃Plus" }
        if ($lower -match "battery doorbell") { return "Ring电池门铃" }
        if ($lower -match "wired doorbell pro") { return "Ring有线门铃Pro" }
        if ($lower -match "wired doorbell") { return "Ring有线门铃" }
        if ($lower -match "video doorbell wired") { return "Ring可视门铃" }
        if ($lower -match "indoor cam plus") { return "Ring室内摄像头Plus" }
        if ($lower -match "indoor cam") { return "Ring室内摄像头" }
        if ($lower -match "outdoor cam plus") { return "Ring室外摄像头Plus" }
        if ($lower -match "outdoor cam") { return "Ring室外摄像头" }
        if ($lower -match "spotlight cam") { return "Ring聚光摄像头" }
        if ($lower -match "floodlight cam") { return "Ring泛光摄像头" }
        if ($lower -match "chime pro") { return "Ring门铃提示器Pro" }
        if ($lower -match "chime") { return "Ring门铃提示器" }
        if ($lower -match "solar panel") { return "Ring太阳能板" }
        if ($lower -match "battery pack") { return "Ring电池包" }
        return "Ring智能家居产品"
    }
    
    # Blink 设备
    if ($lower -match "blink") {
        if ($lower -match "outdoor.*2k") { return "Blink室外摄像头2K" }
        if ($lower -match "outdoor.*floodlight") { return "Blink泛光摄像头" }
        if ($lower -match "outdoor.*xr") { return "Blink室外摄像头XR" }
        if ($lower -match "mini 2k") { return "Blink Mini 2K" }
        if ($lower -match "mini") { return "Blink Mini" }
        return "Blink智能家居产品"
    }
    
    # 制冰机
    if ($lower -match "ice maker") {
        if ($lower -match "nugget") { return "颗粒冰制冰机" }
        if ($lower -match "countertop") { return "台式制冰机" }
        return "制冰机"
    }
    
    # iPhone (非Apple前缀)
    if ($lower -match "iphone (\d+)(?:\s+pro(?:\s+max)?)?") {
        $model = $Matches[1]
        if ($lower -match "pro max") { return "iPhone $model Pro Max" }
        if ($lower -match "pro") { return "iPhone $model Pro" }
        if ($lower -match "plus") { return "iPhone $model Plus" }
        if ($lower -match "mini") { return "iPhone $model Mini" }
        return "iPhone $model"
    }
    
    # AirPods
    if ($lower -match "airpods pro.*2nd") { return "苹果AirPods Pro 2代" }
    if ($lower -match "airpods pro") { return "苹果AirPods Pro" }
    if ($lower -match "airpods (\d)") { return "苹果AirPods $($Matches[1])" }
    
    # PlayStation
    if ($lower -match "playstation.*dualsense") { return "PS5手柄" }
    if ($lower -match "dualsense") { return "PS5手柄" }
    
    # Nintendo
    if ($lower -match "nintendo switch") { return "任天堂Switch" }
    
    # Beats
    if ($lower -match "beats studio pro") { return "Beats Studio Pro" }
    if ($lower -match "beats solo") { return "Beats Solo" }
    
    # 知名品牌直接匹配
    $brandPatterns = @{
        "biodance" = "BIODANCE胶原蛋白面膜"
        "eos.*body lotion" = "eos身体乳"
        "eos.*body wash" = "eos沐浴露"
        "mighty patch" = "Mighty Patch痘痘贴"
        "panoxyl" = "PanOxyl祛痘洗面奶"
        "nizoral" = "Nizoral去屑洗发水"
        "aquaphor" = "Aquaphor修护膏"
        "lodge" = "Lodge铸铁锅"
        "crocs" = "Crocs洞洞鞋"
        "duracell.*2032" = "金霸王2032电池"
        "ninja.*blender" = "Ninja搅拌机"
        "ninja.*air fryer" = "Ninja空气炸锅"
        "cosori.*air fryer" = "Cosori空气炸锅"
        "kitchenaid" = "KitchenAid厨房工具"
        "owala.*freesip" = "Owala FreeSip水杯"
        "stanley.*quencher" = "STANLEY保温杯"
        "yeti.*rambler" = "YETI保温杯"
        "gorilla.*super glue" = "Gorilla强力胶"
        "velcro" = "VELCRO魔术贴"
        "tide.*detergent" = "汰渍洗衣液"
        "clorox.*wipes" = "高乐氏消毒湿巾"
        "lysol.*toilet" = "来苏尔马桶清洁剂"
        "band-aid" = "邦迪创可贴"
        "dove.*body wash" = "多芬沐浴露"
        "tree hut.*scrub" = "Tree Hut磨砂膏"
        "silonn.*ice maker" = "Silonn制冰机"
        "euhomy.*ice maker" = "EUHOMY制冰机"
        "black\+decker" = "Black+Decker电器"
        "rubbermaid.*food storage" = "Rubbermaid食品收纳盒"
        "hotor.*lunch box" = "HOTOR保温饭盒"
        "lifewit.*lunch bag" = "Lifewit午餐包"
        "sensarte.*frying pan" = "SENSARTE不粘锅"
        "reynolds.*parchment" = "Reynolds烘焙纸"
    }
    
    foreach ($pattern in $brandPatterns.Keys) {
        if ($lower -match $pattern) { return $brandPatterns[$pattern] }
    }
    
    # 通用产品类型识别
    if ($lower -match "sunscreen|spf") { return "防晒产品" }
    if ($lower -match "moisturizer|lotion") { return "保湿产品" }
    if ($lower -match "cleanser|face wash") { return "洁面产品" }
    if ($lower -match "serum") { return "精华产品" }
    if ($lower -match "mask") { return "面膜产品" }
    if ($lower -match "shampoo") { return "洗发产品" }
    if ($lower -match "conditioner") { return "护发产品" }
    if ($lower -match "makeup|lipstick|mascara") { return "彩妆产品" }
    if ($lower -match "vitamin|supplement") { return "保健品" }
    if ($lower -match "protein") { return "蛋白产品" }
    if ($lower -match "gloves") { return "手套" }
    if ($lower -match "mask") { return "口罩" }
    if ($lower -match "wipes") { return "湿巾" }
    if ($lower -match "towel") { return "毛巾" }
    if ($lower -match "blanket") { return "毯子" }
    if ($lower -match "pillow") { return "枕头" }
    if ($lower -match "bed") { return "床品" }
    if ($lower -match "chair") { return "椅子" }
    if ($lower -match "table") { return "桌子" }
    if ($lower -match "lamp|light") { return "灯具" }
    if ($lower -match "fan") { return "风扇" }
    if ($lower -match "heater") { return "加热器" }
    if ($lower -match "humidifier") { return "加湿器" }
    if ($lower -match "air purifier") { return "空气净化器" }
    if ($lower -match "vacuum") { return "吸尘器" }
    if ($lower -match "mop") { return "拖把" }
    if ($lower -match "broom") { return "扫帚" }
    if ($lower -match "scale") { return "秤" }
    if ($lower -match "thermometer") { return "温度计" }
    if ($lower -match "timer") { return "计时器" }
    if ($lower -match "battery") { return "电池" }
    if ($lower -match "cable|cord") { return "数据线" }
    if ($lower -match "charger") { return "充电器" }
    if ($lower -match "case") { return "保护壳" }
    if ($lower -match "screen protector") { return "屏幕保护膜" }
    if ($lower -match "headphones|earbuds|earphones") { return "耳机" }
    if ($lower -match "speaker") { return "音箱" }
    if ($lower -match "camera") { return "相机" }
    if ($lower -match "remote") { return "遥控器" }
    if ($lower -match "controller") { return "游戏手柄" }
    if ($lower -match "dog|cat|pet") { return "宠物用品" }
    if ($lower -match "toy") { return "玩具" }
    if ($lower -match "game") { return "游戏" }
    if ($lower -match "book") { return "书籍" }
    if ($lower -match "shoes|sandals|boots") { return "鞋类" }
    if ($lower -match "shirt|tee|top") { return "上衣" }
    if ($lower -match "pants|jeans|shorts") { return "裤子" }
    if ($lower -match "dress|skirt") { return "裙装" }
    if ($lower -match "jacket|coat") { return "外套" }
    if ($lower -match "underwear|bra|panties") { return "内衣" }
    if ($lower -match "bag|backpack|purse") { return "包袋" }
    if ($lower -match "wallet") { return "钱包" }
    if ($lower -match "watch") { return "手表" }
    if ($lower -match "jewelry|necklace|bracelet|ring|earrings") { return "首饰" }
    if ($lower -match "sunglasses|glasses") { return "眼镜" }
    if ($lower -match "hat|cap") { return "帽子" }
    
    # 无法识别的返回原名称截断
    if ($name.Length -gt 15) { return $name.Substring(0, 15) + "..." }
    return $name
}

# 主处理逻辑
Write-Host "读取商品数据..."
$items = Get-Content $INPUT_FILE | ConvertFrom-Json
Write-Host "共 $($items.Count) 个商品"

$results = @()
$count = 0

foreach ($item in $items) {
    $count++
    $shortName = Translate-ProductName $item.name
    
    $results += [PSCustomObject]@{
        id = $item.id
        short_name = $shortName
    }
    
    if ($count % 100 -eq 0) {
        Write-Host "已处理: $count / $($items.Count)"
    }
}

# 输出结果
$output = @{
    batch_id = "translate_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    items = $results
}

Write-Host "保存结果..."
$output | ConvertTo-Json -Depth 3 | Out-File $OUTPUT_FILE -Encoding UTF8
Write-Host "完成！结果已保存到: $OUTPUT_FILE"
