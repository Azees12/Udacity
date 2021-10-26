/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-7e6cm0pp.us', // the auth0 domain prefix
    audience: 'Coffee Stack Shop', // the audience set for the auth0 app
    clientId: 'eF5Q2mDlHAeGn6rKwQpA5jLOwMYtfVBJ', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100/tabs/user-page', // the base url of the running ionic application. 
  }
};

