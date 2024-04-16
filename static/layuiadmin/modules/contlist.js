/** layuiAdmin.std-v1.1.0 LPPL License By http://www.layui.com/admin/ */
;layui.define(["table", "form", 'laydate'], function (e) {
    var t = layui.$, i = layui.table ,l = layui.laydate;
    layui.form;
    i.render({
        elem: "#LAY-member-manage",
        url: "/account/recharge/list",
        cols: [[
            {type: "checkbox", fixed: "left"},
            {field: "id", width: 80, title: "ID", sort: !0},
            {field: "jobNo", title: "工号", minWidth: 100},
            {field: "price", title: "密码", width: 80},
            {field: "name", title: "姓名", width: 80},
            {field: "sex", title: "性别"},
            {field: "position", title: "职位"},
            {field: "phone", title: "联系电话"},
            {field: "dimission", title: "状态"},
            {field: "createTime", title: "添加时间", sort: !0},
            {title: "操作", width: 150, align: "center", fixed: "right", toolbar: "#table-useradmin-webuser"}]],
        page: !0,
        limit: 30,
        height: "full-220",
        text: "对不起，加载出现异常！"
    })
});