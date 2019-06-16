##Description##

So... The project description changed a bit since the time I posted... I think is a bit easier... I would like to go over with you the details... is that ok?


let me explaing trough here....
Your custom authorizer will be invoked by our API Gateway.
The front end will send to API gateway a token (header) and a body request with 3 main informations: OrganizationID, CampusID and Role
On the Token we will send you, your lambda will decrypt the JWT which will contain also the OrganizationID, CampusId and Role information.
The custom authorizer needs to look and see if all the 3 info matches.... That way we can validate the call
Makes sense?

we are using cognito
so we can use cognito's login widget to simulate frontend


I have the APIs ready
you only have to worry wih server side
i'll give you a JWT token and the user's info
M
from there you can use postman to simulate your call and then we can hook on AWS gateway

I was reading a bit more about Custom Authorizer... and I saw that the custom authorizer needs to generate a policy and return that policy to API Gateway correct? To be honest I was a bit lost with that policy thing\


1- Right now we are working on AWS Account which is not the production account... it is just our dev account. So please I need you to instruct me if there is any changes that I should be aware when moving from one account to the other account the lambda authorizer
2- The custom attributes I mentioned earlier (campusID, OrganizationID, Role) we are adding 3 more (environment, region and AccountID). They will all follow the same pattern... whatever is in the token must be in the body request ok?
USD 400


you lambda name is called custom-authorizer
please use the dev-boto3-s3-list-bucket API to do your tests

Awesome. Let me know if you have any questions... by the way you have full privileges with Cognito and API Gateway... Cognito we are only using 1 pool... your user was the last one added and is the only one with all the attributes filled ok?

##AWS Server Info##

https://848149494964.signin.aws.amazon.com/console
user: hong
pass: Internet123#


##Contact##
marceloscharan@gmail.com
scharan_5

Youtube: https://www.youtube.com/watch?v=ItE6MAZaiJY