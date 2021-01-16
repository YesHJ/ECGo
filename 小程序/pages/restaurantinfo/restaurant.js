// pages/restaurantinfo/restaurant.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    name:"",
    location:"",
    phone:"",
    status:"",
    pic:"",
    tag:[],
    isOpen:false,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let temp = app.globalData.resInfo
    let opt = temp[options.id]
    let uistatus = false
    if(opt.status=="Opened")
    {
      uistatus = true
    }
    else
    {
      uistatus = false
    }

    this.setData({
      name: opt.name,
      location: opt.location,
      phone: opt.phone,
      status: opt.status,
      pic: opt.pic,
      tag: opt.tag,
      isOpen: uistatus,
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

  },

  onCall: function(){
    wx.makePhoneCall({
      phoneNumber: this.data.phone,
    })
  },

  queuegoto: function(){
    wx.navigateTo({
      url: '../logs/logs'
    })
  }
})