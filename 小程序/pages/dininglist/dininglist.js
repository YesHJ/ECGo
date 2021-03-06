// pages/dininglist/dininglist.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    qualities: ""
  },

//ListTap
  ListTap(e){
    let a = e.currentTarget.dataset.target
    console.log("AAA = ",a.id)
    let objdata = 'id='+a.id+'&name='+ a.name+'&location='+a.location+'&phone='+a.phone+'&status='+a.status
    wx.navigateTo({
      url: '../restaurantinfo/restaurant?'+objdata
    })
    wx.setStorageSync('rant', a.name)
    console.log("Name = ",a.name)
    app.globalData.currentRestaurant = a.name
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
    this.setData({
        qualities: app.globalData.resInfo,
      })
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