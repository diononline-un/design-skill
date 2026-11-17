const features = [
  { title: "Seamless sync", body: "It's not just a tool, it's a platform for your whole team." },
  { title: "Built for scale", body: "Our engine serves as the cornerstone of modern workflows." },
];
export default function Page() {
  return (
    <main>
      <h1>Elevate your workflow</h1>
      <h2>Welcome back, Damir!</h2>
      <p>Trusted by [number needed] teams. Experts agree it changes everything.</p>
      <button className="flex items-center gap-2 text-sm">Get started</button>
      <button>Save changes.</button>
      <input placeholder="Search anything..." />
      <p>Contact John Doe at example@example.com</p>
      <h3>Why Choose Our Platform</h3>
      <h3>Powerful Features For Teams</h3>
      <h3>Pricing That Scales With You</h3>
    </main>
  );
}
