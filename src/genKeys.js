const assert = require('assert');
const request = require('supertest');
const app = require('./app');

describe('ECDSA', function () {
  let publicKey, privateKey;

  describe('POST /keygen', function () {
    it('should generate a new ECDSA key pair', function (done) {
      request(app)
        .post('/keygen')
        .expect('Content-Type', /json/)
        .expect(200)
        .end(function (err, res) {
          if (err) return done(err);
          publicKey = res.body.publicKey;
          privateKey = res.body.privateKey;
          done();
        });
    });
  });

  describe('POST /:privateKey/:message', function () {
    it('should sign a message with the given private key', function (done) {
      const message = 'hello world';
      request(app)
        .post(`/${privateKey}/${message}`)
        .expect('Content-Type', /json/)
        .expect(200)
        .end(function (err, res) {
          if (err) return done(err);
          const signature = res.body.signature;
          assert(signature);
          done();
        });
    });
  });

  describe('GET /:publicKey/:message/:signature', function () {
    it('should verify a message with the given public key and signature', function (done) {
      const message = 'hello world';
      const signature = signMessage(message, privateKey);
      request(app)
        .get(`/${publicKey}/${message}/${signature}`)
        .expect('Content-Type', /json/)
        .expect(200)
        .end(function (err, res) {
          if (err) return done(err);
          const isValid = res.body.isValid;
          assert(isValid);
          done();
        });
    });
  });
});