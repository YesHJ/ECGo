// index.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    motto: 'Please choose the restaurant',
    userInfo: {},
    hasUserInfo: false,
    canIUseGetUserProfile: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    basicsList: [{
      icon: 'usefullfill',
      name: 'Login'
    }, {
      icon: 'radioboxfill',
      name: 'Choose'
    }, {
      icon: 'radioboxfill',
      name: 'Join'
    }, {
      icon: 'roundcheckfill',
      name: 'Wait'
    }, ],
    index: null,
    picker: ['1', '2', '3','4','5','6','7','8'],
    swiperList: [{
      id: 0,
      type: 'image',
      url: 'http://www.cygia.com/upload/userfiles/images/aboutus/profile/1301F380DCBC55C190D21A32812DEA7C.jpeg'
    }, {
      id: 1,
        type: 'image',
        url: 'http://www.cygia.com/upload/userfiles/images/teamlab/816CE98F9B8E15386665FE47D34E4FD4.jpg',
    }, {
      id: 2,
      type: 'image',
      url: 'http://www.cygia.com/upload/userfiles/images/teamlab/FD3BEB7189187639F3A27066BDECBA4E.jpg'
    }, {
      id: 3,
      type: 'image',
      url: 'http://www.cygia.com/upload/userfiles/images/teamlab/10AC052BCB1FBDB3B2902340CC27789F.jpg'
    }],
  },
  // 请求网络
  getQueueInfoAndGoto: function(){
 
  },
  // 头像点击事件
  bindViewTap() {
    // 这里是获取下发权限地方，根据官方文档，可以根据  wx.getSetting() 的 withSubscriptions   这个参数获取用户是否打开订阅消息总开关。后面我们需要获取用户是否同意总是同意消息推送。所以这里要给它设置为true 。
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
                    tmplIds: [app.globalData.QueueReadymoudle,app.globalData.QueueCanclmoudle,app.globalData.QueueBeforemoudle],
                    success (res) { 
                      if (res[app.globalData.QueueReadymoudle] === 'accept' & res[app.globalData.QueueCanclmoudle] === 'accept'&res[app.globalData.QueueBeforemoudle] === 'accept' ) {
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
                        console.log('拒绝授权 Readymoudle '+res[app.globalData.QueueReadymoudle])
                        console.log('拒绝授权 Readymoudle '+res[app.globalData.QueueCanclmoudle])
                        console.log('拒绝授权 Readymoudle '+res[app.globalData.QueueBeforemoudle])
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
    })
  },
  //卡片切换
  cardSwiper(e) {
    this.setData({
      cardCur: e.detail.current
    })
  },
  //用餐人数选择
  PickerChange(e) {
    console.log(e);
    app.globalData.userNumber = parseInt(e.detail.value) + 1
    this.setData({
      index: e.detail.value
    })
  },
  onLoad() {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
  },
  onShow: function () {
    let userInfoByLocal = wx.getStorageSync('userinfo')
    if (userInfoByLocal) {
      console.log('Has user info,so no need to get userinfo = '+userInfoByLocal.nickName)
      app.globalData.userInfo = userInfoByLocal
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true,
        motto: app.globalData.currentRestaurant,
      })
    } 
  },
  getUserInfo(e) {
    console.log("Use Old Info "+e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },
  getUserProfile(e) {
    // 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认
    // 开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
    wx.getUserProfile({
      desc: '用于完善会员资料', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        wx.setStorageSync('userinfo', res.userInfo)
        app.globalData.userInfo = res.userInfo
        console.log('userInfo 2222 = '+res.userInfo)
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    })
  },
  showModal(e) {
    if(app.globalData.currentRestaurant.indexOf('Please choose')>=0)
    {
      this.setData({
        modalName: e.currentTarget.dataset.target
      })
    }else if(!app.globalData.currentRestaurant)
    {
      this.setData({
        modalName: e.currentTarget.dataset.target
      })
    }
    else
    {
      console.log('cr = '+app.globalData.currentRestaurant.indexOf('Please choose'))
      this.bindViewTap()
    }
  },
  hideModal(e) {
    this.setData({
      modalName: null
    })
  },
})
