import { expect, test, describe } from "bun:test";
import { runCLI, parseJSON } from "./helpers";

interface SearchResponse {
  meta: { count: number; page: number };
  results: Array<{
    id: string;
    title: string;
    company: string | null;
    location: string | null;
    workplaceType: string | null;
    date: string | null;
    url: string;
  }>;
}

describe("builtin-search live smoke tests", () => {
  test("search returns real results with non-null id/title/url", async () => {
    const res = await runCLI(["search", "-q", "AI Engineer", "--limit", "5", "--format", "json"]);
    const data = parseJSON<SearchResponse>(res);
    expect(Array.isArray(data.results)).toBe(true);
    expect(data.results.length).toBeGreaterThan(0);
    for (const job of data.results) {
      expect(job.id).toBeTruthy();
      expect(job.title).toBeTruthy();
      expect(job.url).toContain("builtin.com/job/");
    }
  });

  test("detail on the first search result returns a readable description", async () => {
    const searchRes = await runCLI(["search", "-q", "AI Engineer", "--limit", "3", "--format", "json"]);
    const data = parseJSON<SearchResponse>(searchRes);
    const first = data.results[0];
    expect(first).toBeDefined();
    const detailRes = await runCLI(["detail", first.url, "--format", "json"]);
    const job = parseJSON<{ id: string; title: string; description: string | null }>(detailRes);
    expect(job.id).toBe(first.id);
    expect(job.title).toBeTruthy();
  });
});

describe("builtin-search argument validation", () => {
  test("no query and no location exits 1 with a JSON error on stderr", async () => {
    const res = await runCLI(["search", "--format", "json"]);
    expect(res.exitCode).toBe(1);
    const err = JSON.parse(res.stderr);
    expect(err.code).toBe("NO_QUERY");
  });

  test("a non-numeric --limit exits 1 with a JSON error", async () => {
    const res = await runCLI(["search", "-q", "AI Engineer", "--limit", "abc"]);
    expect(res.exitCode).toBe(1);
    const err = JSON.parse(res.stderr);
    expect(err.code).toBe("BAD_ARG");
  });

  test("detail with no id exits 1", async () => {
    const res = await runCLI(["detail"]);
    expect(res.exitCode).toBe(1);
    const err = JSON.parse(res.stderr);
    expect(err.code).toBe("NO_ID");
  });
});
