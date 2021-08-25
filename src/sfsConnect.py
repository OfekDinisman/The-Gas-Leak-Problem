
# LOCALHOST
LOCAL_CLIENT_ID = "3MVG9I9urWjeUW06Zyk3mHQNYhVa_0CxdgIfv0yI8k2tV.Bh5.m6.Q6WauebvGtxwd.1FRr8EQk2JQ9rGRkwE"
LOCAL_CLIENT_SECRET = "6Cel800D4L000000j49f8884L000000zlqYtvZIdFDaO1s5aDR14WROkIwuM9a8NLJHi2FOo5HcEuegmzyCW9y83BuHGUBWZMOe43T5gNvQ"
LOCAL_REDIRECT_URI = "https://localhost:8443/RestTest/oauth/_callback"

#TODO: CHange to python connection
initParams = { 
    @WebInitParam(name = "clientId", value = 
            "3MVG9lKcPoNINVBJSoQsNCD.HHDdbugPsNXwwyFbgb47KWa_PTv"),
    @WebInitParam(name = "clientSecret", value = "5678471853609579508"),
    @WebInitParam(name = "redirectUri", value = 
            "https://localhost:8443/RestTest/oauth/_callback"),
    @WebInitParam(name = "environment", value = 
            "https://login.salesforce.com/services/oauth2/token")  }
 
HttpClient httpclient = new HttpClient();
PostMethod post = new PostMethod(environment);
post.addParameter("code",code);
post.addParameter("grant_type","authorization_code");

   /** For session ID instead of OAuth 2.0, use "grant_type", "password" **/
post.addParameter("client_id",clientId);
post.addParameter("client_secret",clientSecret);
post.addParameter("redirect_uri",redirectUri);

//exception handling removed for brevity...
  //this is the post from step 2     
  httpclient.executeMethod(post);
     String responseBody = post.getResponseBodyAsString();
   
  String accessToken = null;
  JSONObject json = null;
   try {
       json = new JSONObject(responseBody);
         accessToken = json.getString("access_token");
         issuedAt = json.getString("issued_at");
         /** Use this to validate session 
          * instead of expiring on browser close.
          */
                                
         } catch (JSONException e) {
            e.printStackTrace();
         }
 
         HttpServletResponse httpResponse = (HttpServletResponse)response;
          Cookie session = new Cookie(ACCESS_TOKEN, accessToken);
         session.setMaxAge(-1); //cookie not persistent, destroyed on browser exit
         httpResponse.addCookie(session);