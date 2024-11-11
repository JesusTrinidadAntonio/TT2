const controller={};

controller.login=(req,res)=>{
    res.render('login');
};
controller.signin=(req,res)=>{
    res.render('signin');
};
module.exports=controller;