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
    inQueue:0,
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
    let self = this
    //self.sleep(100)
    wx.request({
      url: app.globalData.host + '/getQueue/',
      method: 'GET',
      header: { 
        "Content-Type": "application/x-www-form-urlencoded"
       }, 
      data: {
        merchant_name : self.data.name,
      },
      success: function (data) {
        let total = 0
        console.log('get queue data = '+app.globalData.host)
        console.log('get queue code = '+data.data.code +' '+ self.data.name)
        console.log('get queue data = '+data.data)
        console.log('get queue data = '+JSON.stringify(data))

        if(data.data.data != null)
        {
          for(var i = 0;i < data.data.data.length;i++)
          {
            let a = data.data.data[i].total
            total = a + total
          }
          console.log('total = '+total)
        }
        self.setData({
          inQueue : total
        })
        console.log(11111111)
      },
      fail: function (res) {
        console.log('指令调用失败'+res.errMsg)
      }
    })
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
  sleep:function(numberMillis) {
    var now = new Date();
    var exitTime = now.getTime() + numberMillis;
    while(true) {
      now = new Date();
      if (now.getTime() > exitTime)
        return;
    }
  },
  onCall: function(){
    wx.makePhoneCall({
      phoneNumber: this.data.phone,
    })
  },
  queuegoto() {
    // 这里是获取下发权限地方，根据官方文档，可以根据  wx.getSetting() 的 withSubscriptions   这个参数获取用户是否打开订阅消息总开关。后面我们需要获取用户是否同意总是同意消息推送。所以这里要给它设置为true 。
    if(app.globalData.userInfo)
    {
    wx.getSetting({
      withSubscriptions: true,   //  这里设置为true,下面才会返回mainSwitch
      success: function(res){   
        // 调起授权界面弹窗
        if (res.subscriptionsSetting.mainSwitch) {  // 用户打开了订阅消息总开关
          if (res.subscriptionsSetting.itemSettings != null) {   // 用户同意总是保持是否推送消息的选择, 这里表示以后不会再拉起推送消息的授权
            let moIdState = res.subscriptionsSetting.itemSettings[app.globalData.QueueReadymoudle,app.globalData.QueueCanclmoudle];  // 用户同意的消息模板id
            if(moIdState === 'accept'){  
              wx.navigateTo({
                url: '../logs/logs'
              })
              console.log('接受了消息推送');
            }else if(moIdState === 'reject'){
              console.log("拒绝消息推送");
            }else if(moIdState === 'ban'){
              console.log("已被后台封禁");
              wx.showToast({
                title: 'System Rejected',//提示文字
                duration:1000,//显示时长
                mask:true,//是否显示透明蒙层，防止触摸穿透，默认：false  
                icon:'loading', //图标，支持"success"、"loading"   
             })
            }
          }else {
            // 当用户没有点击 ’总是保持以上选择，不再询问‘  按钮。那每次执到这都会拉起授权弹窗
            wx.showModal({
              title: '提示',
              content:'请授权开通服务通知',
              showCancel: true,
              success: function (ress) {
                if (ress.confirm) {  
                  wx.requestSubscribeMessage({   // 调起消息订阅界面
                    tmplIds: [app.globalData.QueueReadymoudle,app.globalData.QueueCanclmoudle],
                    success (res) { 
                      if (res[app.globalData.QueueReadymoudle] === 'accept' & res[app.globalData.QueueCanclmoudle] === 'accept' ) {
                        console.log('用户同意授权')
                        wx.navigateTo({
                          url: '../logs/logs'
                        })
                      }else if(res[app.globalData.QueueReadymoudle] != 'accept'){
                        console.log('拒绝授权 Readymoudle '+res[app.globalData.QueueReadymoudle])
                        wx.showToast({
                          title: 'Reject M1',//提示文字
                          duration:1000,//显示时长
                          mask:true,//是否显示透明蒙层，防止触摸穿透，默认：false  
                          icon:'loading', //图标，支持"success"、"loading"  
                          success:function(){ },//接口调用成功
                          fail: function () { },  //接口调用失败的回调函数  
                          complete: function () { } //接口调用结束的回调函数  
                       })
                      } else if(res[app.globalData.QueueCanclmoudle] != 'accept'){
                        console.log('拒绝授权 Cancel moudle '+res[app.globalData.QueueCanclmoudle])
                        wx.showToast({
                          title: 'Reject M2',//提示文字
                          duration:1000,//显示时长
                          mask:true,//是否显示透明蒙层，防止触摸穿透，默认：false  
                          icon:'loading', //图标，支持"success"、"loading"  
                          success:function(){ },//接口调用成功
                          fail: function () { },  //接口调用失败的回调函数  
                          complete: function () { } //接口调用结束的回调函数  
                       })
                      }  
                      else {
                        console.log('拒绝授权')
                        wx.showToast({
                          title: 'User Canceled',//提示文字
                          duration:1000,//显示时长
                          mask:true,//是否显示透明蒙层，防止触摸穿透，默认：false  
                          icon:'loading', //图标，支持"success"、"loading"  
                          success:function(){ },//接口调用成功
                          fail: function () { },  //接口调用失败的回调函数  
                          complete: function () { } //接口调用结束的回调函数  
                       })
                      }
                    },
                    fail (er){
                      console.log("订阅消息 失败 ");
                      console.log(er);
                    }
                  })           
                }
              }
            })
          }
        }else {
          console.log('订阅消息未开启')
        }      
      },
      fail: function(error){
        console.log(error);
      },
    })}else
    {
      wx.showToast({
        title: 'No Login',//提示文字
        duration:1000,//显示时长
        mask:true,//是否显示透明蒙层，防止触摸穿透，默认：false  
        icon:'loading', //图标，支持"success"、"loading"  
        success:function(){ },//接口调用成功
        fail: function () { },  //接口调用失败的回调函数  
        complete: function () { } //接口调用结束的回调函数  
     })
    }
  },
})