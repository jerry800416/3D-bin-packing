**簡要描述：**

- <p>DEMO</p>

**請求URL：**
- 內部 ` http://10.10.19.29:771/showdemo `

- 外部 `  `

**請求方式：**
- GET


 **入參實例**
無

**入參說明：**
無

---
 **出參實例1**

出參
```
{
  "Success": true,
  "data": {
    "box": [
		{
		  "WHD": [560, 244, 259],
		  "partNumber": "Bin",
		  "position": [0, 0, 0],
		  "weight": 28080
		}
	]
    "fitItem": [
      {
        "WHD": [85, 60, 60],
        "color": "yellow",
        "partNumber": "wash17",
        "position": [0, 0, 0],
        "rotationType": 0,
        "type": "wash",
        "weight": 10
      },
      {
        "WHD": [70, 100, 30],
        "color": "blue",
        "partNumber": "Server2",
        "position": [164, 100, 198],
        "rotationType": 1,
        "type": "server",
        "weight": 20
      },
    ],
    "unfitItem": [
      {
        "WHD": [85, 60, 60],
        "color": "yellow",
        "partNumber": "wash10",
        "position": [0, 0, 0],
        "rotationType": 0,
        "type": "wash",
        "weight": 10
      },
      {
        "WHD": [70, 100, 30],
        "color": "blue",
        "partNumber": "Server42",
        "position": [0, 0, 0],
        "rotationType": 5,
        "type": "server",
        "weight": 20
      }
    ]
  }
}
```

----------------------------------------------
**出參說明：**

|參數名|類型|說明|詳細|
|:-----  |:-----|-----                           |
|Success | bool  | 呼叫API成功或失敗 |true 代表入參正確且系統正常運作，false 代表入參錯誤或是系統問題 |
|data |Object   |前端需要的詳細訊息 |包含box,fitItem,unfitItem |
|**box** | **Array**  |**貨櫃資訊** |**包含WHD,position,partNumber,weight**|
|WHD | Array  |貨櫃長寬高 | 第一位代表長(width),第二位代表寬(height),第三位代表高(depth)  |
|position | Array  |該貨櫃起始位置 |第一位代表x,第二位代表y,第三位代表x |
|partNumber | string  |該貨櫃PN碼 | |
|weight | int  |貨櫃承重 |單位為公斤 |
|**fitItem** | **Array**  |**放得進貨櫃的物品資訊** |**包含WHD,color,partNumber,position,rotationType,type,weight** |
|WHD | Array  |物品長寬高 | 第一位代表長(width),第二位代表寬(height),第三位代表高(depth)  |
|color | string  |該物品顏色 |以16進位色碼表示 |
|partNumber | string  |該物品PN碼 | |
|position | Array  |該物品起始位置 |第一位代表x,第二位代表y,第三位代表x |
|rotationType | int  | 該物品的旋轉型態 | 共六個姿態以0-5表示 |
|type | string  | 該物品類型名稱 |  |
|weight | int  |物品重量 |單位為公斤 |


 **備註**
unfitItem 參數和 fitItem 相同
unfitItem 裡面的 position 和 rotationType 無作用