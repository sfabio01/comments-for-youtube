<script>
    import { message } from "./../stores";

    function closeAlert() {
        message.set("");
    }
</script>

{#if $message != ""}
    <div class="alert alert-warning alert-dismissible fade show" role="alert">
        {$message}
        <button
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Close"
            on:click={closeAlert}
        />
    </div>
{/if}
