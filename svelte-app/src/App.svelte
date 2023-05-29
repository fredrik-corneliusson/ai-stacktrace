<script>
    import { Router, Link, Route } from "svelte-routing";
    import Login from "./Login.svelte";
    import Callback from "./Callback.svelte";
    import Main from "./Main.svelte";
    import Logout from "./Logout.svelte";
</script>

<Router>
    <nav>
        <Link to="/">Home</Link>
        <Link to="login">Login</Link>
        <Link to="logout">Logout</Link>
    </nav>
    <div>
        <Route path="/" component={Main} />
        <Route path="/login" component={Login} />
        <Route path="/logout" component={Logout} />
        <Route path="/callback" component={Callback} />
    </div>
</Router>
