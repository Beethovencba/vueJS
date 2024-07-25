import {useAuth} from '@/store/auth.js'

export default async function(to, from, next) {
    if (to.meta?.auth) {
        const auth = useAuth();
        if (auth.token && auth.user) {
          const isAuthenticated = await auth.checkToken();
          
          if (isAuthenticated) {
            next();
          } else {
            next({name: 'login'});  
          }
        } else {
          next({name: 'login'});
        }
    } else {
      next();
    }
}