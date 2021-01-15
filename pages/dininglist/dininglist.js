// pages/dininglist/dininglist.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    qualities: [{
      "id": 0,
      "name": "AAAA",
      "location": "ZhuHai",
      "status": "Closed",
      "pic": "https://ossweb-img.qq.com/images/lol/web201310/skin/big21002.jpg"
    }, {
      "id": 1,
      "name": "BBBBB",
      "location": "ZhuHai",
      "status": "Closed",
      "pic": "https://ossweb-img.qq.com/images/lol/web201310/skin/big21003.jpg"
    }, {
      "id": 2,
      "name": "Star",
      "location": "ZhuHai",
      "status": "Opened",
      "pic": "https://ossweb-img.qq.com/images/lol/web201310/skin/big21004.jpg"
    }, {
      "id": 3,
      "name": "Super",
      "location": "ZhuHai",
      "status": "Opened",
      "pic": "https://ossweb-img.qq.com/images/lol/web201310/skin/big21005.jpg"
    }, {
      "id": 4,
      "name": "TOTS",
      "location": "ZhuHai",
      "status": "Opened",
      "pic": "https://ossweb-img.qq.com/images/lol/web201310/skin/big21006.jpg"
    }, {
      "id": 5,
      "name": "Classic",
      "location": "ZhuHai",
      "status": "Opened",
      "pic": "https://ossweb-img.qq.com/images/lol/web201310/skin/big21007.jpg"
    }, {
      "id": 6,
      "name": "FutureStar",
      "location": "ZhuHai",
      "status": "Opened",
      "pic": "https://ossweb-img.qq.com/images/lol/web201310/skin/big21008.jpg"
    }, {
      "id": 7,
      "name": "Headliners",
      "location": "ZhuHai",
      "status": "Opened",
      "pic": "https://ossweb-img.qq.com/images/lol/web201310/skin/big21009.jpg"
    }, {
      "id": 8,
      "name": "Flashback",
      "location": "ZhuHai",
      "status": "Opened",
      "pic": "https://ossweb-img.qq.com/images/lol/web201310/skin/big21001.jpg"
    }, {
      "id": 9,
      "name": "UCL",
      "location": "ZhuHai",
      "status": "Opened",
      "pic": "https://ossweb-img.qq.com/images/lol/web201310/skin/big21000.jpg"
    }],
  },

//ListTap
  ListTap(e){
    let a = e.currentTarget.dataset.target
    console.log("AAA = ",a)
    wx.navigateTo({
      url: '../restaurantinfo/restaurant?obj='+a
    })
  },

// ListTouch触摸开始
  ListTouchStart(e) {
    this.setData({
      ListTouchStart: e.touches[0].pageX
    })
  },

// ListTouch计算方向
  ListTouchMove(e) {
    this.setData({
      ListTouchDirection: e.touches[0].pageX - this.data.ListTouchStart > 0 ? 'right' : 'left'
    })
  },

// ListTouch计算滚动
  ListTouchEnd(e) {
    if (this.data.ListTouchDirection =='left'){
      this.setData({
        modalName: e.currentTarget.dataset.target
      })
    } else {
      this.setData({
        modalName: null
      })
    }
    this.setData({
      ListTouchDirection: null
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})