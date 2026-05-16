import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name:"landpage",
    component: () => import('../views/LandPage.vue'),
  },
  {
    path: '/login',
    name:"loginpage",
    component: () => import('../views/LoginPage.vue'),
  },
  {
    path: '/register',
    name:"regispage",
    component: () => import('../views/RegisterPage.vue'),
  },
  {
    path: '/admin',
    component: () => import('../views/admin.vue'),
    children:[
      {
        path: '/admin/camp',
        component: () => import('../components/admincamp.vue'),
      },
      {
        path: '/admin/user',
        component: () => import('../components/adminotheruser.vue'),
      },
      {
        path: '/admin/influ/:id',
        component: () => import('../components/admininflu.vue'),
      },
      {
        path: '/admin/spon/:id',
        component: () => import('../components/adminspon.vue'),
      },

      // {
      //   path: '/admin/notifications',
      //   component: () => import('../components/NotifiCompo.vue'),
      // },
      {
        path: '/report',
        component: () => import('../components/report.vue'),
      },
      // {
      //   path: '/admin/warning',
      //   component: () => import('../components/SendWarning.vue'),
      // },
    ],
  },


  {
    path: '/influ',
    component: () => import('../views/influmain.vue'),
    children: [
      {
        path: '/influ/camp/comp/:id',
        component: () => import('../components/campcomp.vue'),
      },
      {
        path: '/influ/camp',
        component: () => import('../components/influothercamp.vue'),
      },
      // {
      //   path: '/influ/noti',
      //   component: () => import('../components/notfification.vue'),
      // },
      {
        path: '/report',
        component: () => import('../components/report.vue'),
      },
      {
        path: '/influ/camp/accep/:id',
        component: () => import('../components/acceptcamp.vue'),
      },
    ],
  },





  
  {
    path: '/spon',
    component: () => import('../views/spon.vue'),
    children: [
      {
        path: '/spon/camp/add',
        component: () => import('../components/createcamp.vue'),
      },
      {
        path: '/spon/camp/edit/:id',
        component: () => import('../components/editcamp.vue'),
      },
      {
        path: '/spon/find/influ/:id',
        component: () => import('../components/findinflu.vue'),
      },
      {
        path: '/spon/notifications',
        component: () => import('../components/notification.vue'),
      },
      {
        path: '/spon/report',
        component: () => import('../components/report.vue'),
      },
    ],
  },
];


const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;




