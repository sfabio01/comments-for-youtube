<script>
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    function loadMore() {
        dispatch("loadMore");
    }
</script>

<div class="container">
    <button
        class="btn btn-primary btn-sm d-block mx-auto my-1"
        on:click={loadMore}
    >
        LOAD MORE
    </button>
</div>
