<script>
    import { message } from "./../stores";
</script>

{#if $message != ""}
    <p>{$message}</p>
{/if}
