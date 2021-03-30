// logs.js
const util = require('../../utils/util.js')
const app = getApp()

Page({
  data: {
    cuMerchart:'test',
    cuType:'S',
    cuUser:'test1',
    cuIndex:'0',
    queueSuc:false,
    queueMsg:'ERR',
    UserInfoForQueue: 'FAIL TO JOIN',
  },
  onLoad(options) {
    console.log(options)
    console.log('User Info'+app.globalData.userInfo)
    let self = this
    let tempName = app.globalData.userInfo.nickName
    let userName = this.encodeUTF8(tempName)
    //TODO 用户名为中文的时候有Bug
    let userNum = app.globalData.userNumber
    let merchart = app.globalData.currentRestaurant
    let tableType = 'small'
    let shorttype = 'S'
    if(userNum>4 && userNum <= 6)
    {
      tableType = 'middle'
      shorttype = 'M'
    }else if(userNum>6)
    {
      tableType = 'big'
      shorttype = 'B'
    }
    console.log('merchart = '+ merchart+';userName = '+userName)
    wx.request({
      url: app.globalData.host + '/refresh',
      method: 'GET',
      header: { 
        "Content-Type": "application/x-www-form-urlencoded"
       }, 
      data: {
        merchant_name : merchart,
        user_name : userName,
      },
      success: function (data) {
        console.log('refresh = '+data.data.index)
        userName = self.decodeUTF8(userName)
        if(data.data.code == -1) //只有没有排队的时候才进行请求
        {
          wx.request({
            url: app.globalData.host + '/line_up',
            method: 'POST',
            header: { 
              "Content-Type": "application/x-www-form-urlencoded"
             }, 
            data: {
              merchant_name : merchart,
              user_name : userName,
              user_id : app.globalData.openCode,
              user_phone : '123456789',
              eat_number : userNum,
              table_type : tableType,
            },
            success: function (data) {
              console.log('line_up = '+data.data.code)
              console.log('tableType = '+tableType)
              console.log('index = '+data.data.index)
              console.log('user_id = '+app.globalData.openCode)
              console.log('name = '+merchart+' line_up '+data.data.message)
              if(data.data.code<0){
                self.setData({
                  cuMerchart : merchart,
                  cuType : shorttype,
                  cuUser : userName,
                  cuIndex : 0,
                  queueSuc : false,
                  queueMsg:'ERR',
                  UserInfoForQueue: userName+' @ '+merchart+ ' err = ' +data.data.message,
                })
              }else{
                self.setData({
                  cuMerchart : merchart,
                  cuType : shorttype,
                  cuUser : userName,
                  cuIndex : data.data.index,
                  queueSuc : true,
                  queueMsg:shorttype+data.data.index,
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
        }else if(data.data.code == -2){
          console.log('no need live_up for '+data.data.message)
          
        }
        else
        {
          console.log(data.data.code+'no need live_up for '+data.data.message)
          //TODO 如果用户已经排队，应该显示队列信息，当前是Undefined信息
          self.setData({
            cuMerchart : merchart,
            cuType : shorttype,
            cuUser : userName,
            cuIndex : data.data.index,
            queueSuc : true,
            queueMsg : shorttype+data.data.index,
            UserInfoForQueue: userName+' @ '+merchart+' USER NUMBER = '+userNum,
          })
        }
      }
    })
    
  },
  onReady: function () {

  },
  queuecancel: function(){
    let self = this
    wx.request({
      url: app.globalData.host + '/passNum',
      method: 'GET',
      header: { 
        "Content-Type": "application/x-www-form-urlencoded"
       }, 
      data: {
        merchant_name : self.data.cuMerchart,
        table_type : self.data.cuType,
        table_index : self.data.cuIndex,
        user : self.data.cuUser,
      },
      success: function (data) {
        console.log('PASS Num '+data.data.message)
        wx.navigateBack();
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
       wx.navigateBack();
    },
    })
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
  },
  encodeUTF8:function (str) {
    return str.replace(/[^\u0000-\u00FF]/g, function ($0) { return escape($0).replace(/(%u)(\w{4})/gi, "&#x$2;") }); 
  },
  decodeUTF8:function(str) {
    return unescape(str.replace(/&#x/g, '%u').replace(/\\u/g, '%u').replace(/;/g, ''));
  }
})
