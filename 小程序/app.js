// app.js
App({
  onLaunch() {
    // 展示本地存储能力
    let rant = wx.getStorageSync('rant')
    console.log("rant = " + rant)
    if(rant==null || rant.length == 0)
    {
      rant = "Please choose the restaurant"
    }else{
      console.log(222222)
    } 
    this.globalData.currentRestaurant = rant
    wx.setStorageSync('rant', rant)  
    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        console.log('login code ='+res.code); // 先login得到code
        if (res.code) {
        // 将url中的appid和secret换成自己的  （可以在开发平台查看）
          this.globalData.openCode = res.code
        }
      }
    })
    // 获取用户信息
  },
  onShow: function () {
    console.log('Show APP')
    this.getMerchantInfo()
  },
  getMerchantInfo: function () {
    let self = this
    wx.request({
      url: this.globalData.host + '/searchMerchant/',
      method: 'GET',
      success: function (data) {
        console.log('data = '+data.data.message)
        console.log('Merchant data = '+data.data.data)
        if(data.data.data != ''){
          let pic = "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fbjcache.leju.com%2Fzxjiaju%2Fzx_pic%2F20180509%2Fa0%2F67%2Fa670d844ebf06b368575a111aee6397c.jpeg&refer=http%3A%2F%2Fbjcache.leju.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1613294165&t=4bf09f335633fabe1ffee855883a4b7a"
          let list = data.data.data
          let qualities = []
          for(var i = 0;i < list.length;i++)
          {
            let item = data.data.data[i]
            console.log(item)
            let status = 'Closed'
            let location = 'No address is record'
            let phone = 'No Number'
            let tag = ["Environment","Hot"]
            self.getMercharDetail(item.name)
            if(item.enable == true)
            {
              status = 'Opened'
            }
            if(item.location != '' && item.location != null)
            {
              location = item.location
            }
            if(item.phone != '' && item.phone != null)
            {
              phone = item.phone
            }
            qualities.push({
              id: i,
              name: item.name,
              location: location,
              phone: phone,
              status: status,
              pic: pic,
              tag:tag,
            })
          }
          self.globalData.resInfo = qualities
        }else
        {
          wx.showToast({
            title: 'Server Error',//提示文字
            duration:1000,//显示时长
            mask:true,//是否显示透明蒙层，防止触摸穿透，默认：false  
            icon:'loading', //图标，支持"success"、"loading"   
         })
        }
      }
    })
  },
  getMercharDetail: function (merchart) {
    let self = this
    wx.request({
      url: this.globalData.host + '/commitConfig',
      method: 'GET',
      header: { 
        "Content-Type": "application/x-www-form-urlencoded"
       }, 
      data: {
        merchant_name : merchart,
      },
      success: function (data) {
        self.updateMerchantInfo(merchart,data.data.merchant_phone,data.data.merchant_position)
      }
    })
  },
  updateMerchantInfo: function (merchant,phone,position) {
    for(var i = 0;i < this.globalData.resInfo.length;i++)
    {
      if(this.globalData.resInfo[i].name == merchant)
      {
        this.globalData.resInfo[i].phone = phone
        this.globalData.resInfo[i].location = position
        console.log('position data = '+this.globalData.resInfo[i].location)
        console.log('phone data = '+this.globalData.resInfo[i].phone)
      }
    }
    console.log(this.globalData.resInfo)
  },

  globalData: {
    userInfo: null,
    openCode: null,
    host: 'https://www.snail2651.com',
    currentRestaurant: "Please Choose the restaurant",
    lastTime: "",
    userNumber: 1,
    appID: 'wx9dc3a069c71ba1af',
    key: '46c445a802736b5a068f29bc787d5160',
    QueueReadymoudle: "lKl7yagNE8783YzK7_NnAI6sSSK3ECgBQxCeolD9ISw",
    QueueCanclmoudle: "XV3X3kjwxtsZXce-0pa7zggvyKQMWjBs5iWHygSjPsQ",
    resInfo: [{
      "id": 0,
      "name": "For Test1",
      "location": "ZhuHai-AAA-GGG-Road22",
      "phone": "12345678901",
      "status": "Closed",
      "tag": ["Environment","many people"],
      "pic": "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fbjcache.leju.com%2Fzxjiaju%2Fzx_pic%2F20180509%2Fa0%2F67%2Fa670d844ebf06b368575a111aee6397c.jpeg&refer=http%3A%2F%2Fbjcache.leju.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1613294165&t=4bf09f335633fabe1ffee855883a4b7a"
    }, {
      "id": 1,
      "name": "For Test2",
      "location": "ZhuHai-AAA-GGG-Road22",
      "phone": "12345678901",
      "status": "Closed",
      "tag": ["Environment","Delicious"],
      "pic": "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fbjcache.leju.com%2Fzxjiaju%2Fzx_pic%2F20161118%2Fde%2F96%2Fd96e483ca1f45a406ad2151c4ed46a63.jpeg&refer=http%3A%2F%2Fbjcache.leju.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1613294165&t=9ee35ba84b49efb6747b1e2d32e4f115"
    }, {
      "id": 2,
      "name": "For Test3",
      "location": "ZhuHai-AAA-GGG-Road22",
      "phone": "12345678901",
      "status": "Closed",
      "tag": ["Environment","Delicious"],
      "pic": "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fpic1.shejiben.com%2Fcase%2F1208%2F11%2F20120811_26c7748df20b4169aaeaaoY939dnfjmX.jpg&refer=http%3A%2F%2Fpic1.shejiben.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1613294165&t=6282d21c65db23825cd23ffb9e9681b4"
    }, {
      "id": 3,
      "name": "For Test4",
      "location": "ZhuHai-AAA-GGG-Road22",
      "phone": "12345678901",
      "status": "Closed",
      "tag": ["Environment","Price"],
      "pic": "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fpic1.shejiben.com%2Fcase%2F2016%2F07%2F18%2F20160718104437-73843fc2.jpg&refer=http%3A%2F%2Fpic1.shejiben.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1613294165&t=10ea9c3a8accf5148c180cca3cec9ac5"
    }, {
      "id": 4,
      "name": "For Test5",
      "location": "ZhuHai-AAA-GGG-Road22",
      "phone": "12345678901",
      "status": "Closed",
      "tag": ["Environment","Delicious"],
      "pic": "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fm.tuniucdn.com%2Ffilebroker%2Fcdn%2Fsnc%2F57%2Ffc%2F57fc55155e4e8404f19b484088afd96f_w800_h400_c1_t0.jpg&refer=http%3A%2F%2Fm.tuniucdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1613294165&t=2c77d5c79e4f99c310ac9229bd3b88f5"
    }],
  }
})
