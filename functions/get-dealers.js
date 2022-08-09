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
    if (params.st) {
      // return dealership with this state
      cloudant
        .postFind({ db: "dealerships", selector: { st: params.st } })
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
    } else if (params.id) {
      id = parseInt(params.dealerId);
      // return dealership with this id
      cloudant
        .postFind({
          db: "dealerships",
          selector: {
            id: parseInt(params.id),
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
    } else {
      // return all documents
      cloudant
        .postAllDocs({ db: "dealerships", includeDocs: true, limit: 10 })
        .then((result) => {
          let code = 200;
          if (result.result.rows.length == 0) {
            code = 404;
          }
          resolve({
            statusCode: code,
            headers: { "Content-Type": "application/json" },
            body: result.result.rows,
          });
        })
        .catch((err) => {
          reject(err);
        });
    }
  });
}

let result = main({});
result.then((dealers) => console.log(dealers));
