// logs.js
const util = require('../../utils/util.js')
const app = getApp()

Page({
  data: {
    queueSuc:false,
    queueMsg:'ERR',
    UserInfoForQueue: 'FAIL TO JOIN',
  },
  onLoad(options) {
    console.log(options)
    console.log(app.globalData.userInfo.nickName)
    let userName = app.globalData.userInfo.nickName
    let userNum = app.globalData.userNumber
    let merchart = app.globalData.currentRestaurant
    wx.request({
      url: app.globalData.host + '/line_up/',
      method: 'POST',
      data: null,
      success: function (data) {
        console.log('line_up = '+data)
        this.setData(
          {
            queueSuc:true,
            queueMsg:10,
            UserInfoForQueue: userName+' @ '+merchart+' USER NUMBER = '+userNum
          }
        )
      },
      fail: function(){
          wx.showToast({
            title: 'NetWork Error',//提示文字
            duration:1000,//显示时长
            mask:true,//是否显示透明蒙层，防止触摸穿透，默认：false  
            icon:'loading', //图标，支持"success"、"loading"  
            success:function(){ },//接口调用成功
            fail: function () { },  //接口调用失败的回调函数  
            complete: function () { } //接口调用结束的回调函数  
         })
      },
    })
  },

  queuecancel: function(){
    wx.navigateBack();
  },
  queuegoto: function(){
    wx.navigateTo({
      url: '../logs/logs'
    })
  }

})
