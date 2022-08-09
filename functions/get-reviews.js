function main(params) {
  return new Promise(function (resolve, reject) {
    const { CloudantV1 } = require("@ibm-cloud/cloudant");
    const { IamAuthenticator } = require("ibm-cloud-sdk-core");
    const authenticator = new IamAuthenticator({
      apikey: "iA7PjkYuT5Anc1OT7mg3waHZ3lE2Fi1kBt8Hc54WdBm0",
    });
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator,
    });
    cloudant.setServiceUrl(
      "https://ef1704d4-d45c-43e3-8bde-7d9c1e768096-bluemix.cloudantnosqldb.appdomain.cloud"
    );
    dealership = parseInt(params.dealerId);
    // return reviews with this dealer id
    cloudant
      .postFind({
        db: "reviews",
        selector: {
          dealership: parseInt(params.dealerId),
        },
      })
      .then((result) => {
        let code = 200;
        if (result.result.docs.length == 0) {
          code = 404;
        }
        resolve({
          statusCode: code,
          headers: { "Content-Type": "application/json" },
          body: result.result.docs,
        });
      })
      .catch((err) => {
        reject(err);
      });
  });
}

// example invocation
let result = main({ dealerId: 15 });
result.then((reviews) => console.log(reviews));
