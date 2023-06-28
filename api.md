
# API DOC

### Outline
- [API DOC](#api-doc)
    - [Outline](#outline)
    - [getAllData (TODO)](#getalldata-todo)
    - [calPacking](#calpacking)



### getAllData (TODO)

```
            "level":0,
            "loadbear":50,
            "weight":170,
            "color" :5
        },
        {
            "name":"Moving Box",
            "WHD" : [60,40,50],
            "count":80 ,
            "updown":1,
            "type":1,
            "level":0,
            "loadbear":40,
            "weight":30,
            "color" :6
        },
        {
            "name":"Wood Table",
            "WHD" : [152,152,75],
            "count":10 ,
            "updown":1,
            "type":1,
            "level":0,
            "loadbear":50,
            "weight":70,
            "color" :7
        }
    ]
}
```

**出參說明：**

參數名|類型|說明|詳細
:-----:  |:-----:|:-----: |:-----:                      
**box** |**Object **  |**貨櫃信息** |**包含name,weight,openTop,coner** 
<font color="red">name</font> | String  |貨櫃名稱 | 貨櫃顯示名稱(唯一值)  
<font color="red">WHD</font> | Array(int)  |貨櫃長寬高 | 貨櫃長寬高  
<font color="red">weight</font> |  Integer  |該貨櫃最大可承受重量 |單位為KG
openTop | Array  |該貨櫃支持的開門型態 |1代表可一般側開，2代表可頂開 
coner | int  |角件邊長大小 |0代表無角件，1開始有角件，單位為公分 
**item** | **Object**  |**物品信息** |**name,count,updown,type,level,loadbear,weight,color** 
<font color="red">name</font> | String  |貨物名稱 | 貨物顯示名稱(唯一值)  
count | Integer  |該貨物數量 |單位為個 
updown | Integer  |該貨物是否可以倒放 |0: false，1 : true 
<font color="red">type</font> | Integer  |該物品型態 |1:立方體, 2: 圓柱體  
level | Integer  | 該物品是否必須裝箱 | 0: false，1 : true 
<font color="red">loadbear</font> | Integer  | 該物品承受重量 | 單位為公斤 
<font color="red">weight</font> | Integer  | 該物品重量 | 單位為公斤 
color | Integer  |物品顯示顏色 |1:紅2:黃3:藍4:綠5:紫6:棕7:橙 
​
**備註**
此出參結構和前端要返回計算的結構相同
紅色字體代表不能夠讓user修改的值，其餘可以讓user修改


### calPacking

**簡要描述：**

- <p>前端送出貨物和貨櫃資訊，並取回計算結果</p>

**請求URL：**
- 內部 ` http://10.10.19.29:771/calPacking `

- 外部 `  `

**請求方式：**
- POST

**入參實例**
```
{
    "box": [
        {
            "name": "40呎超高貨櫃",
			"WHD" : [1203,235,269],
            "weight": 26280,
            "openTop": [1,2],
            "coner":15
        }
    ],
    "item": [
        {
            "name":"Dyson_DC34_Animal",
			"WHD" : [170,82,46],
            "count":5 ,
            "updown":1,
            "type":1,
            "level":0,
            "loadbear":100,
            "weight":85,
            "color" :1
        },
        {
            "name":"Panasonic_NA-V160GBS",
			"WHD" : [85,60,60],
            "count":18 ,
            "updown":1,
            "type":1,
            "level":0,
            "loadbear":100,
            "weight":30,
            "color" :2
        },
        {
            "name":"Superlux_RS921",
			"WHD" : [60,80,200],
            "count":15 ,
            "updown":1,
            "type":1,
            "level":0,
            "loadbear":10,
            "weight":30,
            "color" :3
        },
        {
            "name":"Dell_R740",
			"WHD" : [70,100,30],
            "count":30 ,
            "updown":1,
            "type":1,
            "level":0,
            "loadbear":100,
            "weight":20,
            "color" :4
        },
        {
            "name":"50_Gal_Oil_Drum",
			"WHD" : [80,80,120],
            "count":20 ,
            "updown":0,
            "type":2,
            "level":0,
            "loadbear":50,
            "weight":170,
            "color" :5
        },
        {
            "name":"Moving_Box",
			"WHD" : [60,40,50],
            "count":25 ,
            "updown":1,
            "type":1,
            "level":0,
            "loadbear":40,
            "weight":30,
            "color" :6
        },
        {
            "name":"Wood_Table",
			"WHD" : [152,152,75],
            "count":2 ,
            "updown":1,
            "type":1,
            "level":0,
            "loadbear":50,
            "weight":70,
            "color" :7
        }
    ],
	"binding" : [
        [
           "Wood_Table",
           "50_Gal_Oil_Drum"
        ],
    ]
}
```

**入參說明：**

參數名|類型|說明|詳細
:-----:  |:-----:|:-----:|:-----:
|**box** |**Object **  |**貨櫃信息** |**包含name,weight,openTop,coner** |
|name| String  |貨櫃名稱 | 貨櫃顯示名稱(唯一值)  |
|WHD | Array(int)  |貨櫃長寬高 | 貨櫃長寬高  |
|weight |  Integer  |該貨櫃最大可承受重量 |單位為KG|
|openTop | Array  |該貨櫃支持的開門型態 |1代表一般側開，2代表頂開 |
|coner | int  |角件邊長大小 |0代表無角件，1開始有角件，單位為公分 |
|**item** | **Object**  |**物品信息** |**name,count,updown,type,level,loadbear,weight,color** |
|name | String  |貨物名稱 | 貨物顯示名稱(唯一值)  |
|count | Integer  |該貨物數量 |單位為個 |
|updown | Integer  |該貨物是否可以倒放 |0: false，1 : true |
|type| Integer  |該物品型態 |1:立方體, 2: 圓柱體  |
|level | Integer  | 該物品是否必須裝箱 | 0: false，1 : true |
|loadbear | Integer  | 該物品承受重量 | 單位為公斤 |
|weight | Integer  | 該物品重量 | 單位為公斤 |
|color | Integer  |物品顯示顏色 |1:紅2:黃3:藍4:綠5:紫6:棕7:橙 |
|**binding** | **Array**  |**物品綁定數量** |**array** |

**出參實例**
```
{
    "Success": true,
    "data": {
        "box": [
            {
                "WHD": [
                    1203,
                    235,
                    238
                ],
                "gravity": [
                    26.37,
                    25.95,
                    27.88,
                    19.79
                ],
                "partNumber": "40呎鋼製貨櫃",
                "position": [
                    601.5,
                    117.5,
                    119.0
                ],
                "weight": 26480
            }
        ],
        "fitItem": [
            {
                "WHD": [
                    15,
                    15,
                    15
                ],
                "color": "#000000",
                "name": "corner",
                "partNumber": "corner0",
                "position": [
                    7,
                    7,
                    7
                ],
                "rotationType": 0,
                "type": "cube",
                "weight": 0
            },
            {
                "WHD": [
                    170,
                    82,
                    46
                ],
                "color": "red",
                "name": "Dyson_DC34_Animal",
                "partNumber": "Dyson_DC34_Animal-13",
                "position": [
                    935,
                    123,
                    23
                ],
                "rotationType": 0,
                "type": "cube",
                "weight": 85
            },
            {
                "WHD": [
                    70,
                    100,
                    30
                ],
                "color": "green",
                "name": "Dell_R740",
                "partNumber": "Dell_R740-7",
                "position": [
                    895,
                    50,
                    61
                ],
                "rotationType": 0,
                "type": "cube",
                "weight": 20
            }
        ],
        "unfitItem": [
            {
                "WHD": [
                    152,
                    75,
                    152
                ],
                "color": "orange",
                "name": "Wood_Table",
                "partNumber": "Wood_Table-8",
                "position": [
                    76,
                    37,
                    76
                ],
                "rotationType": 5,
                "type": "cube",
                "weight": 70
            },
            {
                "WHD": [
                    152,
                    75,
                    152
                ],
                "color": "orange",
                "name": "Wood_Table",
                "partNumber": "Wood_Table-9",
                "position": [
                    76,
                    37,
                    76
                ],
                "rotationType": 5,
                "type": "cube",
                "weight": 70
            }
        ]
    }
}
```

**出參說明：**

|參數名|類型|說明|詳細|
|:-----:  |:-----:|:-----:|:-----:|
|Success | bool  | 呼叫API成功或失敗 |true 代表入參正確且系統正常運作，false 代表入參錯誤或是系統問題 |
|data |Object   |前端需要的詳細訊息 |包含box,fitItem,unfitItem |
|**box** | **Array**  |**貨櫃資訊** |**包含WHD,position,partNumber,weight**|
|WHD | Array  |貨櫃長寬高 | 第一位代表長(width),第二位代表寬(height),第三位代表高(depth)  |
|position | Array  |該貨櫃起始位置 |第一位代表x,第二位代表y,第三位代表x |
|partNumber | string  |該貨櫃PN碼 | |
|weight | int  |貨櫃承重 |單位為公斤 |
|gravity | Array  |貨櫃四等分的重量分佈 |單位為比例(%) |
|**fitItem** | **Array**  |**放得進貨櫃的物品資訊** |**包含WHD,color,partNumber,position,rotationType,type,weight** |
|WHD | Array  |物品長寬高 | 第一位代表長(width),第二位代表寬(height),第三位代表高(depth)  |
|color | string  |該物品顏色 |以16進位色碼表示 |
|partNumber | string  |該物品PN碼 | |
|position | Array  |該物品起始位置 |第一位代表x,第二位代表y,第三位代表x |
|rotationType | int  | 該物品的旋轉型態 | 共六個姿態以0-5表示 |
|name | string  | 該物品類型名稱 |  |
|type | string  | 該物品是立方體還是圓柱體 |cube 代表方，cylinder代表圓柱體  |
|weight | int  |物品重量 |單位為公斤 |

 **備註**
unfitItem 參數和 fitItem 相同