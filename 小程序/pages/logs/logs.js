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
    let self = this
    let userName = app.globalData.userInfo.nickName
    let userNum = app.globalData.userNumber
    let merchart = app.globalData.currentRestaurant
    let tableType = 'small'
    if(userNum>4 && userNum <= 6)
    {
      tableType = 'middle'
    }else
    {
      tableType = 'big'
    }
    wx.request({
      url: app.globalData.host + '/refresh',
      method: 'GET',
      data: {
        merchant_name : merchart,
        user_name : userName,
      },
      success: function (data) {
        console.log('refresh = '+data.data.message)
        if(data.data.code == -1) //只有没有排队的时候才进行请求
        {
          wx.request({
            url: app.globalData.host + '/line_up',
            method: 'POST',
            data: {
              merchant_name : merchart,
              user_name : userName,
              user_phone : null,
              eat_number : userNum,
              table_type : tableType,
            },
            success: function (data) {
              console.log('line_up = '+data.data.code)
              console.log('line_up = '+data.data.message)
              if(data.data.code<0)
              {
                self.setData({
                  queueSuc : false,
                  queueMsg:'ERR',
                  UserInfoForQueue: userName+' @ '+merchart+ 'err = ' +data.data.message,
                })
              }else
              {
                wx.setStorageSync("viewTitle", 'ERR')
                wx.setStorageSync("viewInfo", userName+' @ '+merchart+' USER NUMBER = '+userNum)
                wx.setStorageSync("viewStatus", false)
                self.setData({
                  queueSuc : false,
                  queueMsg:'ERR',
                  UserInfoForQueue: userName+' @ '+merchart+' USER NUMBER = '+userNum,
                })
              }
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
        }else
        {
          console.log('no need live_up for '+data.data.message)
        }
      }
    })
    
  },
  onReady: function () {

  },
  queuecancel: function(){
    wx.navigateBack();
  },
  queuegoto: function(){
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  sleep:function(numberMillis) {
    var now = new Date();
    var exitTime = now.getTime() + numberMillis;
    while(true) {
      now = new Date();
      if (now.getTime() > exitTime)
        return;
    }
  }
})
