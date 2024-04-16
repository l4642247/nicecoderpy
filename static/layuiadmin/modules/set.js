/** layuiAdmin.std-v1.1.0 LPPL License By http://www.layui.com/admin/ */
;layui.define(["form", "upload", "laydate", 'HttpRequest'], function (t) {
    var i = layui.$, e = layui.layer, a = (layui.laytpl, layui.setter, layui.view, layui.admin), n = layui.form,
        s = layui.upload, l = layui.laydate , HttpRequest = layui.HttpRequest;
    i("body");
    n.verify({
        name: function (t, i) {
            return new RegExp("^[a-zA-Z0-9_一-龥\\s·]+$").test(t) ? /(^\_)|(\__)|(\_+$)/.test(t) ? "用户名首尾不能出现下划线'_'" : /^\d+\d+\d$/.test(t) ? "用户名不能全为数字" : void 0 : "用户名不能有特殊字符"
        },
        pass: [/^[\S]{6,12}$/, "密码必须6到12位，且不能出现空格"],
        repass: function (t) {
            if (t !== i("#LAY_password").val()) return "两次密码输入不一致"
        }
    }), n.on("submit(set_website)", function (t) {
        return e.msg(JSON.stringify(t.field)), !1
    }), n.on("submit(set_system_email)", function (t) {
        return e.msg(JSON.stringify(t.field)), !1
    }), n.on("submit(setmyinfo)", function (t) {
        var httpRequest = new HttpRequest("/user/save", 'post', function (data) {
            return e.msg(data.msg), !1
        }, function (data) {
            return e.msg(data.msg), !1
        });
        httpRequest.set(t.field);
        httpRequest.start(true);
    });
    var r = i("#LAY_avatarSrc");
    s.render({
        url: "/file/upload/", elem: "#LAY_avatarUpload", done: function (t) {
            0 == t.code ? r.val(t.data.src) : e.msg(t.msg, {icon: 5})
        }
    }), a.events.avartatPreview = function (t) {
        var i = r.val();
        e.photos({photos: {title: "查看头像", data: [{src: i}]}, shade: .01, closeBtn: 1, anim: 5})
    }, n.on("submit(setmypass)", function (t) {
        var httpRequest = new HttpRequest("/user/passwordModify", 'post', function (t) {
            if(0 == t.code){
                e.msg(t.msg, {icon: 1})
                // setTimeout("parent.layui.admin.events.closeThisTabs()", 2000 )
            }else{
                e.msg(t.msg, {icon: 5})
            }
        });
        httpRequest.set(t.field);
        httpRequest.start(true);
    }), t("set", {})
});