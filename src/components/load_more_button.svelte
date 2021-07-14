<script>
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    function loadMore() {
        dispatch("loadMore");
    }
</script>

<button on:click={loadMore}>LOAD MORE</button>
