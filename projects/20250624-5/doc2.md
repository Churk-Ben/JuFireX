# 项目结构和基础代码



以下是基于 **纯 HTML/CSS/JavaScript + Flask** 的轻量化项目结构及基础代码，不使用 React 框架，更适合快速原型开发或教学演示场景：



---



### **项目结构**



```bash

.

├── backend/                  # Flask后端

│   ├── app.py               # 主入口

│   ├── config.py            # 数据库配置

│   ├── requirements.txt     # 依赖库

│   ├── models/             # 数据模型

│   │   └── models.py

│   ├── utils/              # 工具类

│   │   ├── gis_utils.py    # GIS计算工具

│   │   └── recommender.py  # 推荐算法

│   └── data/               # 模拟数据

│       └── sample_data.csv

└── frontend/                # 静态前端

    ├── index.html           # 主页面

    ├── css/

    │   └── style.css        # 全局样式

    ├── js/

    │   ├── api.js           # 接口调用

    │   └── map.js           # 地图逻辑

    └── assets/              # 静态资源

        ├── markers/         # 地图标记图标

        └── products/        # 商品图片

```



---



### **项目依赖**



#### **`requirements.txt`**



```text

# 基础框架

Flask==2.3.2             # 后端Web框架

Flask-CORS==3.0.10       # 处理跨域请求



# 地理计算

geopy==2.3.0             # 地理距离计算（核心GIS依赖）



# 数据库（可选，若需持久化数据）

# SQLAlchemy==2.0.19     # ORM框架

# psycopg2-binary==2.9.6 # PostgreSQL适配器

# geoalchemy2==0.13.5    # PostGIS扩展支持



# 机器学习（可选，若需复杂推荐算法）

# scikit-learn==1.3.0    # 基础机器学习库

# lightgbm==4.1.0        # 梯度提升树模型



# 开发工具

python-dotenv==1.0.0     # 环境变量管理（用于配置敏感信息）

```



---



#### **依赖分类说明**



1. **必需依赖**（MVP 原型必须安装）



   - `Flask` + `Flask-CORS`：快速搭建 API 并解决前端跨域问题。

   - `geopy`：核心 GIS 功能（计算空间权重、距离衰减）。



2. **可选依赖**（按需扩展）



   - **数据库**：若需连接 PostgreSQL+PostGIS，取消注释`SQLAlchemy`相关行。

   - **推荐算法**：若需替换为机器学习模型，添加`scikit-learn`或`lightgbm`。



3. **开发辅助**

   - `python-dotenv`：管理数据库密码等敏感配置（如`.env`文件）。



---



#### **常见问题**



1. **安装`geopy`失败**



   - 确保 Python 版本 ≥3.7，或尝试升级 pip：

     ```bash

     pip install --upgrade pip

     ```



2. **需要更轻量化的 GIS 计算**  

   可替换为纯数学实现的`haversine`公式库（减少依赖）：



   ```text

   haversine==2.8.0

   ```



3. **PostGIS 连接问题**  

   确保已安装 PostgreSQL 并启用 PostGIS 扩展，然后在`config.py`中配置连接字符串。



---



### **后端代码（Flask）**



#### 1. `app.py` - 主入口



```python

from flask import Flask, jsonify, request

from flask_cors import CORS

from utils.gis_utils import calculate_spatial_weight

from utils.recommender import generate_recommendations

import config



app = Flask(__name__)

CORS(app)  # 允许跨域请求



# 模拟数据（实际应连接数据库）

sample_products = [

    {"id": 1, "name": "西湖龙井", "lat": 30.23, "lng": 120.12, "price": 150, "tags": ["茶叶", "杭州"]},

    {"id": 2, "name": "内蒙古牛肉干", "lat": 40.82, "lng": 111.67, "price": 80, "tags": ["肉类", "草原"]}

]



@app.route('/recommend', methods=['POST'])

def recommend():

    # 获取用户位置（纬度、经度）

    data = request.json

    user_lat = data.get('lat')

    user_lng = data.get('lng')



    # 计算空间权重并生成推荐列表

    recommendations = generate_recommendations(user_lat, user_lng, sample_products)

    return jsonify(recommendations)



if __name__ == '__main__':

    app.run(debug=True, port=5000)

```



#### 2. `utils/gis_utils.py` - GIS 工具类



```python

from geopy.distance import geodesic



def calculate_spatial_weight(user_coord, item_coord, lambda_param=0.01):

    """

    计算用户与商品的空间权重（指数衰减）

    :param user_coord: 用户坐标 (lat, lng)

    :param item_coord: 商品坐标 (lat, lng)

    :param lambda_param: 衰减系数

    :return: 权重值 (0~1)

    """

    distance = geodesic(user_coord, item_coord).km

    return round(2.71828 ** (-lambda_param * distance), 2)  # e^(-λd)

```



#### 3. `utils/recommender.py` - 推荐算法



```python

def generate_recommendations(user_lat, user_lng, products):

    """

    生成推荐列表（示例：空间权重排序）

    :param user_lat: 用户纬度

    :param user_lng: 用户经度

    :param products: 商品列表

    :return: 按权重排序后的推荐列表

    """

    user_coord = (user_lat, user_lng)

    for product in products:

        item_coord = (product['lat'], product['lng'])

        product['weight'] = calculate_spatial_weight(user_coord, item_coord)

    return sorted(products, key=lambda x: x['weight'], reverse=True)[:5]  # 返回Top5

```



---



### **前端代码（静态）**



#### 2. 前端 `frontend/index.html`



```html

<!DOCTYPE html>

<html lang="zh-CN">

  <head>

    <meta charset="UTF-8" />

    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>特产推荐平台</title>

    <link rel="stylesheet" href="css/style.css" />

    <!-- Leaflet地图库 -->

    <link

      rel="stylesheet"

      href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"

    />

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  </head>

  <body>

    <div class="container">

      <h1>基于GIS的特产推荐</h1>

      <button id="refreshBtn">获取我的位置</button>

      <div id="map"></div>

      <div id="productList" class="product-list"></div>

    </div>



    <script src="js/api.js"></script>

    <script src="js/map.js"></script>

  </body>

</html>

```



#### 3. 样式 `frontend/css/style.css`



```css

/* 基础样式 */

body {

  font-family: "Helvetica Neue", Arial, sans-serif;

  margin: 0;

  padding: 0;

  background-color: #f5f5f5;

}



.container {

  max-width: 800px;

  margin: 0 auto;

  padding: 20px;

}



#refreshBtn {

  background-color: #1677ff;

  color: white;

  border: none;

  padding: 10px 15px;

  border-radius: 4px;

  cursor: pointer;

  margin-bottom: 15px;

}



/* 地图容器 */

#map {

  height: 300px;

  width: 100%;

  border-radius: 8px;

  margin-bottom: 20px;

  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

}



/* 商品列表 */

.product-list {

  display: grid;

  gap: 10px;

}



.product-item {

  background: white;

  padding: 12px;

  border-radius: 6px;

  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

}



.product-price {

  color: #ff4d4f;

  font-weight: bold;

}

```



#### 4. 地图逻辑 `frontend/js/map.js`



```javascript

// 初始化地图

const map = L.map("map").setView([30.23, 120.12], 5);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {

  attribution: "© OpenStreetMap",

}).addTo(map);



// 自定义图标

const customIcon = L.icon({

  iconUrl: "assets/markers/pin.png",

  iconSize: [32, 32],

  popupAnchor: [0, -15],

});



// 刷新位置按钮事件

document.getElementById("refreshBtn").addEventListener("click", () => {

  if (navigator.geolocation) {

    navigator.geolocation.getCurrentPosition((position) => {

      const { latitude, longitude } = position.coords;

      getRecommendations(latitude, longitude);

    });

  } else {

    alert("您的浏览器不支持地理位置功能");

  }

});



// 渲染推荐结果

function renderProducts(products) {

  const container = document.getElementById("productList");

  container.innerHTML = products

    .map(

      (product) => `

        <div class="product-item">

            <h3>${product.name}</h3>

            <p class="product-price">¥${product.price}</p>

            <p>推荐权重: ${product.weight}</p>

        </div>

    `

    )

    .join("");

}

```



#### 5. API 交互 `frontend/js/api.js`



```javascript

async function getRecommendations(lat, lng) {

  try {

    const response = await fetch("http://localhost:5000/recommend", {

      method: "POST",

      headers: { "Content-Type": "application/json" },

      body: JSON.stringify({ lat, lng }),

    });

    const data = await response.json();



    // 渲染地图标记

    map.eachLayer((layer) => {

      if (layer instanceof L.Marker) map.removeLayer(layer);

    });



    data.forEach((product) => {

      L.marker([product.lat, product.lng], { icon: customIcon })

        .addTo(map)

        .bindPopup(`<b>${product.name}</b><br>权重: ${product.weight}`);

    });



    // 渲染列表

    renderProducts(data);

  } catch (error) {

    console.error("请求失败:", error);

  }

}

```



---



### **运行步骤**



1. 安装依赖



```bash

cd backend

pip install -r requirements.txt

```



2. 启动后端服务



```bash

cd backend

python app.py

```



3. 前端访问

   - 直接打开`frontend/index.html`文件（需解决 CORS 问题）

   - 或使用 Live Server 扩展（VSCode 插件）访问`http://127.0.0.1:5500/frontend/`



---



### **优化点**



1. **移动端适配**  

   在`style.css`中添加：



   ```css

   @media (max-width: 600px) {

     .container {

       padding: 10px;

     }

     #map {

       height: 250px;

     }

   }

   ```



2. **加载状态提示**  

   在`api.js`中添加：



   ```javascript

   function showLoading() {

     document.getElementById("productList").innerHTML =

       '<div class="loading">加载中...</div>';

   }

   ```



3. **本地存储缓存**  

   缓存用户位置：

   ```javascript

   localStorage.setItem("lastPosition", JSON.stringify({ lat, lng }));

   ```



---



### **与前方案对比**



| 特性           | React 方案         | 纯 HTML/JS 方案        |
| -------------- | ------------------ | ---------------------- |
| **开发复杂度** | 较高（需构建工具） | 极低（直接浏览器运行） |
| **性能**       | 优（虚拟 DOM）     | 良（直接 DOM 操作）    |
| **适合场景**   | 复杂交互应用       | 快速原型/教学演示      |
| **GIS 集成**   | 需要 React-Leaflet | 直接使用 Leaflet 库    |



---



> 这种方案保留了核心的 GIS 推荐功能，**去除了所有复杂的前端工具链**

>

> 如需扩展功能（如用户登录），可以逐步添加 jQuery 或 Vue.js 等轻量级库。



---



### **关键界面示例**



| 功能         | 描述                                                         |
| ------------ | ------------------------------------------------------------ |
| **地图展示** | 显示用户位置与推荐商品产地标记，点击标记显示商品名称和权重值 |
| **推荐列表** | 滚动列表展示商品名称、价格和推荐权重，支持下拉刷新           |

