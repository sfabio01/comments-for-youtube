<script>
    export let msg = "";
</script>

{#if msg != ""}
    <p style="color: red;">{msg}</p>
{/if}
