import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [{ duration: "30s", target: 1000 }],
};

export default function () {
  const res = http.get(
    "https://t-user-service-b4jwrdrecq-ew.a.run.app/users/1"
  );
  check(res, {
    "is status 200": (r) => r.status === 200,
  });
  sleep(1);
}
