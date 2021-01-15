// index.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    motto: 'Please choose the restaurant',
    userInfo: {},
    hasUserInfo: false,
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
    }, {
      id: 4,
      type: 'image',
      url: 'http://www.cygia.com/upload/userfiles/images/teamlab/D5DBAA56D821A8EF9CDAB8A0D8EA88D1.jpg'
    }, {
      id: 5,
      type: 'image',
      url: 'http://www.cygia.com/upload/userfiles/images/teamlab/6C8653959F7893338B24EACFE964317D.jpg'
    }, {
      id: 6,
      type: 'image',
      url: 'http://www.cygia.com/upload/userfiles/images/teamlab/F3FD3FCE29883CBBF8DAA7D66FF79F5C.jpg'
    }],
  },
  // 头像点击事件
  bindViewTap() {
    wx.navigateTo({
      url: '../logs/logs'
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
    this.setData({
      index: e.detail.value
    })
  },
  onLoad() {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse) {
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  }
})
